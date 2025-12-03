# Sprint Plan: Smart Pins Tutorial Comprehensive Audit & Enhancement

**Sprint Name:** smart-pins-tutorial-audit-sprint
**Created:** 2025-12-02
**Status:** PLANNING
**Target Document:** `engineering/document-production/manuals/p2-smart-pins-tutorial/opus-master-green-book/P2-Smart-Pins-Green-Book-Tutorial.md`

---

## Sprint Objective

Perform comprehensive audit of the Smart Pins Tutorial against the P2 Knowledge Base YAML, correct all errors, and add missing content to create an authoritative, production-ready tutorial.

---

## Phase 1: Critical Corrections (Mode Number/Name Errors)

### 1.1 Fix Synchronous/Asynchronous Serial Mode Numbers
**Priority:** CRITICAL
**Issue:** Tutorial has wrong mode numbers for serial modes

| Current (WRONG) | Correct (YAML) |
|-----------------|----------------|
| %11010 = Sync TX | %11010 = ADC Scope Trigger |
| %11011 = Async RX | %11011 = USB Host/Device |
| %11100 = Async TX | %11100 = Sync Serial TX |
| (missing) | %11101 = Sync Serial RX |
| (missing) | %11110 = Async Serial TX |
| ADC listed wrong | %11111 = Async Serial RX |

**Tasks:**
- [ ] Fix Appendix A mode reference table (lines 3254-3287)
- [ ] Fix all serial mode sections in Chapter content
- [ ] Verify all code examples use correct mode constants

### 1.2 Fix PWM Mode Names (Swapped)
**Priority:** CRITICAL
**Issue:** Triangle and Sawtooth are reversed

| Current (WRONG) | Correct (YAML) |
|-----------------|----------------|
| %01000 = PWM Sawtooth | %01000 = PWM Triangle |
| %01001 = PWM Triangle | %01001 = PWM Sawtooth |

**Tasks:**
- [ ] Swap all references to PWM Triangle/Sawtooth
- [ ] Update code examples with correct constants
- [ ] Fix Appendix A table

### 1.3 Fix NCO/Transition Mode Names (Shifted)
**Priority:** CRITICAL
**Issue:** Modes %00101-%00111 have wrong names

| Current (WRONG) | Correct (YAML) |
|-----------------|----------------|
| %00101 = NCO Frequency | %00101 = Transition Output |
| %00110 = NCO Duty | %00110 = NCO Frequency |
| %00111 = Transition | %00111 = NCO Duty |

**Tasks:**
- [ ] Correct all mode name references
- [ ] Update all affected code examples
- [ ] Fix Appendix A table

### 1.4 Fix DAC Mode Descriptions
**Priority:** HIGH
**Issue:** Modes %00010-%00011 incorrectly described as impedance values

| Current (WRONG) | Correct (YAML) |
|-----------------|----------------|
| %00010 = DAC 124Ω 3.3V | %00010 = DAC 16-bit PRNG Dither |
| %00011 = DAC 75Ω 2.0V | %00011 = DAC 16-bit PWM Dither |

**Tasks:**
- [ ] Correct DAC mode descriptions
- [ ] Clarify that impedance values are configuration bits, not modes
- [ ] Update Appendix A table

---

## Phase 2: New Content - A/B Input Routing

### 2.1 Add Clock Pin Routing Section
**Priority:** CRITICAL
**Issue:** Tutorial doesn't explain how to specify clock pin location for serial modes

**Content to add:**
- Explanation of A-input and B-input routing
- Constants: P_LOCAL_A/B, P_PLUS1_A/B, P_PLUS2_A/B, P_PLUS3_A/B, P_MINUS1_A/B, etc.
- Examples showing clock on adjacent pins
- Common patterns for SPI (MOSI/MISO/CLK relationships)

**Tasks:**
- [ ] Write new section "Understanding A/B Input Routing"
- [ ] Add routing examples to all serial mode sections
- [ ] Create table of all routing constants with hex values

---

## Phase 3: New Content - Output Mode Comparison

### 3.1 Add Output Generation Modes Comparison Chapter
**Priority:** HIGH
**Issue:** Tutorial doesn't explain when to use Pulse vs Transition vs NCO vs PWM

**Content to add:**
- Comparison table of all 7 output modes
- Decision tree/flowchart for mode selection
- P_PULSE vs P_TRANSITION detailed comparison
- P_NCO_FREQ vs P_NCO_DUTY detailed comparison
- P_PWM_TRIANGLE vs P_PWM_SAWTOOTH detailed comparison
- P_PWM_SMPS special use case
- Practical examples showing same task with different modes

**Tasks:**
- [ ] Write comparison chapter (~3-5 pages)
- [ ] Create decision flowchart (text-based or TikZ)
- [ ] Add code examples demonstrating mode differences

---

## Phase 4: New Content - Polling, Events, and High Performance

### 4.1 Add Smart Pin Polling vs Events Section
**Priority:** HIGH
**Issue:** Tutorial doesn't cover event-driven Smart Pin usage

**Content to add:**
- Polling methods: TESTP, PINREAD loops
- Event-based waiting: SETSE1/WAITSE1
- When to use each approach
- CPU utilization comparison
- Code examples for both approaches

**Tasks:**
- [ ] Write polling patterns section
- [ ] Write event-based patterns section
- [ ] Add comparison table
- [ ] Include PASM2 and Spin2 examples

### 4.2 Add High-Performance Patterns Chapter
**Priority:** HIGH
**Issue:** Tutorial doesn't cover overlapped operations

**Content to add:**
- Starting multiple Smart Pins while waiting for others
- Double-buffering techniques
- Multi-cog Smart Pin coordination
- Pipelining Smart Pin operations
- Real timing considerations

**Tasks:**
- [ ] Write overlapped operations section
- [ ] Write double-buffering section
- [ ] Add multi-cog coordination examples
- [ ] Include performance tips

### 4.3 Add IN Flag Management Section
**Priority:** MEDIUM
**Issue:** RDPIN/RQPIN/AKPIN not fully explained

**Content to add:**
- RDPIN - Read AND acknowledge (clears IN)
- RQPIN - Read WITHOUT acknowledging (preserves IN)
- AKPIN - Acknowledge without reading (clears IN)
- When to use each
- Multi-cog access patterns

**Tasks:**
- [ ] Write IN flag management section
- [ ] Add use case examples for each instruction
- [ ] Explain multi-cog considerations

---

## Phase 5: P_ Constants and D-Code Documentation

### 5.1 Update All Code Examples with Constants and D-Codes
**Priority:** HIGH
**Issue:** Examples don't show hex values alongside constants

**Format to use:**
```spin2
mode := P_SYNC_TX | P_OE | P_PLUS1_B
' D-code: $11_00_01C0
' Binary: %0001_0001_000_0000000000000_01_11100_0
```

**Tasks:**
- [ ] Update all Spin2 examples with D-code comments
- [ ] Update all PASM2 examples with D-code comments
- [ ] Ensure consistent format throughout

### 5.2 Create Appendix: Complete Constants Reference with Bit Decodes
**Priority:** HIGH
**Issue:** No comprehensive constants reference with bit patterns

**Content to add:**
- All P_ constants (Smart Pin relevant) organized by category
- Hex value for each constant
- Binary bit pattern for each constant (ALL bits shown, no ellipses)
- Structured table with bit fields broken out into columns

**Table Format (bit fields as columns, all 32 bits visible):**
```
┌──────────────┬──────────┬────────┬────────┬─────────┬───────────────┬────────┬───────┐
│ Constant     │ Hex      │ A[3:0] │ B[3:0] │ FFF     │ M[12:0]       │ TT     │ SSSSS │
│              │          │ Input  │ Input  │ Filter  │ Low Level     │ Dir/Out│ Mode  │
├──────────────┼──────────┼────────┼────────┼─────────┼───────────────┼────────┼───────┤
│ P_SYNC_TX    │ $0000001C│ 0000   │ 0000   │ 000     │ 0000000000000 │ 00     │ 11100 │
│ P_OE         │ $01000000│ 0000   │ 0000   │ 000     │ 0000000000000 │ 01     │ 00000 │
│ P_PLUS1_B    │ $00010000│ 0000   │ 0001   │ 000     │ 0000000000000 │ 00     │ 00000 │
└──────────────┴──────────┴────────┴────────┴─────────┴───────────────┴────────┴───────┘
```

**Categories to cover:**
- Mode constants (P_NORMAL through P_ADC) - all 32 modes
- A-input routing (P_LOCAL_A, P_PLUS1_A, P_PLUS2_A, P_PLUS3_A, P_MINUS1_A, P_MINUS2_A, P_MINUS3_A, P_OUTBIT_A)
- B-input routing (P_LOCAL_B, P_PLUS1_B, P_PLUS2_B, P_PLUS3_B, P_MINUS1_B, P_MINUS2_B, P_MINUS3_B, P_OUTBIT_B)
- Input polarity (P_TRUE_A, P_INVERT_A, P_TRUE_B, P_INVERT_B)
- Input options (P_SCHMITT_A, P_SCHMITT_B, P_SCHMITT_AB)
- Output control (P_OE, P_INVERT_OUTPUT)
- DAC configuration (P_DAC_990R_3V, P_DAC_600R_2V, P_DAC_124R_3V, P_DAC_75R_2V)
- ADC configuration (P_ADC_GIO, P_ADC_VIO, P_ADC_FLOAT, P_ADC_1X, P_ADC_3X, P_ADC_10X, P_ADC_30X, P_ADC_100X)
- Filtering (P_FILT0, P_FILT1, P_FILT2, P_FILT3)
- Drive strength (P_HIGH_FAST, P_HIGH_1K5, P_HIGH_15K, P_HIGH_150K, P_HIGH_1MA, P_HIGH_100UA, P_HIGH_10UA, P_HIGH_FLOAT, P_LOW_FAST, P_LOW_1K5, P_LOW_15K, P_LOW_150K, P_LOW_1MA, P_LOW_100UA, P_LOW_10UA, P_LOW_FLOAT)

**Tasks:**
- [ ] Create comprehensive constants appendix with structured bit-field table
- [ ] Show ALL bits in each field (no ellipses)
- [ ] Annotate column headers with bit field names and bit ranges
- [ ] Verify all values against YAML knowledge base
- [ ] Include both hex and broken-out binary representation

---

## Phase 6: Final Review and Cleanup

### 6.1 Remove/Update Placeholder Markers
**Priority:** MEDIUM

**Tasks:**
- [ ] Find and address all `::: needs-diagram` markers
- [ ] Find and address all `::: needs-technical-review` markers
- [ ] Find and address all `::: needs-verification` markers
- [ ] Find and address all `::: needs-examples` markers
- [ ] Find and address all `::: preliminary-content` markers

### 6.2 Verify Cross-References and Index
**Priority:** MEDIUM

**Tasks:**
- [ ] Verify all internal cross-references are valid
- [ ] Update index entries for new content
- [ ] Check page number references (will need update after PDF)

### 6.3 Final Consistency Check
**Priority:** MEDIUM

**Tasks:**
- [ ] Verify all mode numbers match YAML throughout document
- [ ] Verify all constants are correctly named
- [ ] Verify all code examples are syntactically correct
- [ ] Check for any remaining inconsistencies

---

## Deliverables

1. **Updated Master Document:** `P2-Smart-Pins-Green-Book-Tutorial.md` with all corrections and new content
2. **Version Tag:** Git tag marking completed audit version
3. **Sprint Summary:** Documentation of all changes made

---

## Estimated Effort

| Phase | Description | Estimate |
|-------|-------------|----------|
| Phase 1 | Critical Corrections | 2-3 hours |
| Phase 2 | A/B Input Routing | 1-2 hours |
| Phase 3 | Output Mode Comparison | 2-3 hours |
| Phase 4 | Polling/Events/Performance | 3-4 hours |
| Phase 5 | Constants & D-Codes | 3-4 hours |
| Phase 6 | Final Review | 1-2 hours |
| **Total** | | **12-18 hours** |

---

## Dependencies and Prerequisites

- Access to P2KB YAML files for authoritative reference
- Current master document in opus-master-green-book
- Model: Opus 4.1 recommended for content generation quality

---

## Post-Sprint Actions (NOT part of this sprint)

1. Move completed master to workspace
2. Apply PDF production adaptations
3. Generate production PDF
4. Technical review of generated PDF

---

## Questions for Review - RESOLVED

1. **Phase ordering:** ✅ My discretion - foundation work first, dependent work after

2. **Constants appendix size:** ✅ All P_ constants (Smart Pin relevant ~100-150), not all 1200+

3. **Code example format:** ✅ Verbose with hex AND binary, PLUS structured table with bit fields broken into columns (all bits shown, no ellipses)

4. **TikZ diagrams:** ✅ Include new diagrams where they help explain concepts not already covered

5. **Scope check:** ✅ Complete as documented

---

**Status:** APPROVED - Ready for execution. See MCP todos tagged `smart_pins` for sequenced work items.
