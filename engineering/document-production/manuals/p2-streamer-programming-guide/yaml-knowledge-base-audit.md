# YAML Knowledge Base Audit - Streamer Content

**Audit Date:** 2026-01-22
**Audited Against:** P2 Streamer Programming Guide v1.0
**Purpose:** Identify gaps and errors in YAML knowledge base streamer content

---

## Executive Summary

The YAML knowledge base has significant gaps and errors in streamer documentation. The most critical issues are:

1. **DAC routing table is incorrect** - wrong mappings in architecture file
2. **Pin group selection is wrong** - shows 8-pin groups instead of 32-pin blocks
3. **Symbols file is severely incomplete** - claims 85 symbols, only ~8 defined
4. **XZERO description is wrong everywhere** - described as "stream zeros" instead of "zero phase"
5. **Instruction YAMLs lack examples and details** - xcont, xzero, setxfrq are sparse

---

## File-by-File Analysis

### 1. `deliverables/ai/P2/architecture/streamer.yaml`

**Status:** Needs major corrections

#### Issue 1.1: DAC Mapping Table INCORRECT

**Current (WRONG):**
```yaml
mapping_table:
  0b0000: "No DAC output"
  0b0001: "X0 → all four DACs"
  0b0010: "X1 → all four DACs"
  0b0011: "X0 → DAC0/1, X1 → DAC2/3"
```

**Correct (from Silicon Doc):**
```yaml
mapping_table:
  0b0000: "No DAC output (X_DACS_OFF)"
  0b0001: "X0 on all channels (X_DACS_0_0_0_0)"
  0b0010: "X0 on channels 0,1 (X_DACS_X_X_0_0)"
  0b0011: "X0 on channels 2,3 (X_DACS_0_0_X_X)"
  0b0100: "X0 on channel 0 only (X_DACS_X_X_X_0)"
  0b0101: "X0 on channel 1 only (X_DACS_X_X_0_X)"
  0b0110: "X0 on channel 2 only (X_DACS_X_0_X_X)"
  0b0111: "X0 on channel 3 only (X_DACS_0_X_X_X)"
  0b1000: "Differential pairs X0/!X0 (X_DACS_0N0_0N0)"
  0b1001: "Differential on 0,1 (X_DACS_X_X_0N0)"
  0b1010: "Differential on 2,3 (X_DACS_0N0_X_X)"
  0b1011: "Stereo X1,X0 pairs (X_DACS_1_0_1_0)"
  0b1100: "Stereo on 0,1 (X_DACS_X_X_1_0)"
  0b1101: "Stereo on 2,3 (X_DACS_1_0_X_X)"
  0b1110: "Differential stereo (X_DACS_1N1_0N0)"
  0b1111: "All 4 independent (X_DACS_3_2_1_0)"
```

#### Issue 1.2: Pin Group Selection INCORRECT

**Current (WRONG):**
```yaml
groups:
  - "Group 0: Pins 0-7"
  - "Group 1: Pins 8-15"
  # ... 8-pin groups
```

**Correct (from Silicon Doc):**
```yaml
groups:
  - "%000: Pins 31..0"
  - "%001: Pins 39..8"
  - "%010: Pins 47..16"
  - "%011: Pins 55..24"
  - "%100: Pins 63..32"
  - "%101: Pins 7..0, 63..40 (wrap)"
  - "%110: Pins 15..0, 63..48 (wrap)"
  - "%111: Pins 23..0, 63..56 (wrap)"
```

#### Issue 1.3: Mode Numbers Don't Match Silicon Doc

**Current:** Uses abstract mode numbers [0], [1], [2,3]...

**Correct:** Should use D[31:28] encoding:
- `%0000`-`%0011`: Immediate → LUT → Pins/DACs
- `%0100`-`%0111`: Immediate → Pins/DACs
- `%0111` (+ config): RDFAST → LUT → Pins/DACs
- `%1000`-`%1011`: RDFAST → Pins/DACs
- `%1011` (+ config): RGB modes
- `%1100`-`%1111`: Capture modes
- `%1111_x111`: DDS/Goertzel

---

### 2. `deliverables/ai/P2/language/pasm2/xcont.yaml`

**Status:** Needs enhancement

**Issues:**
- Description has typo: "Bu er" instead of "Buffer"
- No examples
- No explanation of phase continuation
- No use case documentation

**Recommended additions:**
```yaml
description: Buffer new streamer command to execute on final NCO rollover, continuing phase.

examples:
- context: Seamless video line streaming
  code: |
    ' Chain visible pixels with blanking without gaps
    xinit   m_visible, #0     ' Start 640 visible pixels
    xcont   m_front, sync0    ' Queue 16 front porch
    xcont   m_sync, sync1     ' Queue 96 sync pulse
    xcont   m_back, sync0     ' Queue 48 back porch
    waitxfi

- context: Continuous audio streaming
  code: |
    ' Seamless DAC output with phase continuity
    rdfast  #0, ##audio_buffer
    xinit   audio_mode, #0
    xcont   audio_mode, #0    ' Chain next buffer seamlessly

patterns:
- name: Command Chaining
  description: |
    XCONT buffers a command that executes when the current command's
    count expires. Phase continuity prevents audio pops and timing glitches.
    
notes:
- Phase continues from previous command (no reset)
- Use for seamless data streaming where timing matters
- Must have active command - use XINIT to start
```

---

### 3. `deliverables/ai/P2/language/pasm2/xzero.yaml`

**Status:** Needs enhancement

**Issues:**
- Description has typo: "Bu er" instead of "Buffer"
- No examples
- No explanation of phase zeroing purpose
- Wrong description in concepts file

**Recommended additions:**
```yaml
description: Buffer new streamer command to execute on final NCO rollover, zeroing NCO phase.

examples:
- context: Video line timing reset
  code: |
    ' Zero phase at each line start prevents drift accumulation
    line:
      xzero   m_sync, sync1     ' Sync pulse, phase zeroed
      xcont   m_back, sync0     ' Back porch
      xcont   m_visible, #0     ' Visible pixels
      xcont   m_front, sync0    ' Front porch
      jmp     #line

- context: Precise timing alignment
  code: |
    ' Reset phase for known timing reference
    xzero   timing_mode, #0   ' Restart with known phase

notes:
- Phase is zeroed when command begins execution
- Use at video line boundaries to prevent accumulated drift
- Essential for multi-line video timing accuracy
- Does NOT stream zeros - zeros the NCO phase accumulator
```

---

### 4. `deliverables/ai/P2/language/pasm2/setxfrq.yaml`

**Status:** Needs major enhancement

**Issues:**
- No frequency calculation formula
- No common values table
- No SETQ alternative method
- No +1 trick for fractional values

**Recommended additions:**
```yaml
frequency_calculation:
  formula: "frequency = $8000_0000 × (desired_rate / clock_frequency)"
  note: "For fractional ratios, add 1 to ensure proper initial rollover"

common_values:
  - ratio: "1:1"
    value: "$8000_0000"
    description: "Every clock"
  - ratio: "1:2"
    value: "$4000_0000"
    description: "Half clock rate"
  - ratio: "1:3"
    value: "$2AAA_AAAB"
    description: "Third clock rate (+1 for fractional)"
  - ratio: "1:10"
    value: "$0CCC_CCCD"
    description: "Tenth clock rate (25MHz at 250MHz)"

alternative_method:
  description: "Use SETQ before XINIT/XCONT/XZERO for atomic frequency change"
  example: |
    setq    ##$0CCC_CCCD    ' Set frequency inline
    xinit   mode, data      ' Execute with new frequency

video_rates:
  - resolution: "640×480"
    pixel_rate: "25.175 MHz"
    at_250mhz: "$0CCC_CCCD"
    at_300mhz: "$0AAA_AAAB"
```

---

### 5. `deliverables/ai/P2/language/spin2/symbols/spin2-builtin-symbols-complete.yaml`

**Status:** SEVERELY INCOMPLETE

**Issue:** Claims 85 streamer symbols but only defines ~8

**Missing symbols (HIGH PRIORITY):**

**Mode symbols (~40 missing):**
- `X_IMM_16X2_LUT`, `X_IMM_8X4_LUT`, `X_IMM_4X8_LUT`
- `X_IMM_32X1_1DAC1`, `X_IMM_16X2_2DAC1`, `X_IMM_16X2_1DAC2`
- `X_IMM_8X4_4DAC1`, `X_IMM_8X4_2DAC2`, `X_IMM_8X4_1DAC4`
- `X_RFBYTE_1P_1DAC1`, `X_RFBYTE_2P_2DAC1`, `X_RFBYTE_4P_4DAC1`
- `X_RFBYTE_8P_1DAC8`, `X_RFWORD_16P_4DAC4`, `X_RFWORD_16P_2DAC8`
- `X_RFLONG_32P_4DAC8`
- `X_RFBYTE_LUMA8`, `X_RFBYTE_RGBI8`, `X_RFBYTE_RGB8`
- `X_RFWORD_RGB16`, `X_RFLONG_RGB24`
- `X_1P_1DAC1_WFBYTE`, `X_2P_2DAC1_WFBYTE`, `X_4P_4DAC1_WFBYTE`
- `X_32P_4DAC8_WFLONG`
- `X_1ADC8_0P_1DAC8_WFBYTE`, `X_2ADC8_0P_2DAC8_WFWORD`
- `X_DDS_GOERTZEL_SINC1`, `X_DDS_GOERTZEL_SINC2`

**DAC symbols (16 missing):**
- `X_DACS_OFF`, `X_DACS_0_0_0_0`, `X_DACS_X_X_0_0`
- `X_DACS_0_0_X_X`, `X_DACS_X_X_X_0`, `X_DACS_X_X_0_X`
- `X_DACS_X_0_X_X`, `X_DACS_0_X_X_X`, `X_DACS_0N0_0N0`
- `X_DACS_X_X_0N0`, `X_DACS_0N0_X_X`, `X_DACS_1_0_1_0`
- `X_DACS_X_X_1_0`, `X_DACS_1_0_X_X`, `X_DACS_1N1_0N0`
- `X_DACS_3_2_1_0`

**Control symbols (4 missing):**
- `X_WRITE_OFF`, `X_WRITE_ON`
- `X_ALT_OFF`, `X_ALT_ON`

---

### 6. `concepts/streamer_smartpin_control.yaml`

**Status:** Has critical error

**Issue:** XZERO description is WRONG

**Current (WRONG):**
```yaml
XZERO:
  syntax: "XZERO mode, count"
  operation: "Stream zeros (no hub read)"
  use: "Generate timing/clocks"
```

**Correct:**
```yaml
XZERO:
  syntax: "XZERO {#}D,{#}S"
  operation: "Buffer command to execute on final NCO rollover, zeroing phase"
  use: "Video line timing reset, phase alignment"
  note: "Does NOT stream zeros - zeros the NCO phase accumulator"
```

---

### 7. `engineering/knowledge-base/P2-support/components/streamer.yaml`

**Status:** Needs correction

**Issue:** XZERO misleadingly described

**Current:**
```yaml
config: XZERO - Zero streamer state
```

**Correct:**
```yaml
phase_reset: XZERO - Buffer command with phase zero on execution
```

---

## Recommended Actions

### Priority 1 (Critical - Data Errors)

| File | Action |
|------|--------|
| `architecture/streamer.yaml` | Fix DAC mapping table with correct values and symbol names |
| `architecture/streamer.yaml` | Fix pin group selection to 32-pin blocks |
| `concepts/streamer_smartpin_control.yaml` | Fix XZERO description |
| `components/streamer.yaml` | Fix XZERO description |

### Priority 2 (High - Missing Content)

| File | Action |
|------|--------|
| `symbols/spin2-builtin-symbols-complete.yaml` | Add all 80+ missing streamer symbols |
| `pasm2/xcont.yaml` | Add examples and patterns |
| `pasm2/xzero.yaml` | Add examples and patterns |
| `pasm2/setxfrq.yaml` | Add frequency calculation, common values, SETQ method |

### Priority 3 (Medium - Enhancement)

| File | Action |
|------|--------|
| `pasm2/xinit.yaml` | Add command word structure details |
| `pasm2/getxacc.yaml` | Add QVECTOR pattern, SINC1/SINC2 context |
| `pasm2/xstop.yaml` | Add equivalence to `XINIT #0,#0` |
| `architecture/streamer.yaml` | Add complete mode encoding table |

---

## Symbol Value Reference

For completing the symbols file, here are the correct values:

```yaml
# Mode symbols
X_IMM_32X1_LUT: "$0000_0000"      # %0000 << 28
X_IMM_16X2_LUT: "$1000_0000"      # %0001 << 28
X_IMM_8X4_LUT: "$2000_0000"       # %0010 << 28
X_IMM_4X8_LUT: "$3000_0000"       # %0011 << 28
X_IMM_32X1_1DAC1: "$4000_0000"    # %0100 << 28
X_RFBYTE_1P_1DAC1: "$8000_0000"   # %1000 << 28
X_RFWORD_RGB16: "$B005_0000"      # %1011 << 28 + 5<<16
X_DDS_GOERTZEL_SINC1: "$F007_0000" # %1111 << 28 + 7<<16
X_DDS_GOERTZEL_SINC2: "$F087_0000" # %1111 << 28 + $87<<16

# Control symbols
X_PINS_OFF: "$0000_0000"          # %0 << 23
X_PINS_ON: "$0080_0000"           # %1 << 23
X_WRITE_OFF: "$0000_0000"         # %0 << 23
X_WRITE_ON: "$0080_0000"          # %1 << 23
X_ALT_OFF: "$0000_0000"           # %0 << 16
X_ALT_ON: "$0001_0000"            # %1 << 16

# DAC symbols
X_DACS_OFF: "$0000_0000"          # %0000 << 24
X_DACS_0_0_0_0: "$0100_0000"      # %0001 << 24
X_DACS_X_X_0_0: "$0200_0000"      # %0010 << 24
X_DACS_3_2_1_0: "$0F00_0000"      # %1111 << 24
```

---

## Verification Checklist

After corrections, verify:

- [ ] DAC routing: `%0001` = X0 on all channels (not X0→all four DACs differently)
- [ ] Pin groups: `%000` = Pins 31..0 (32-pin blocks, not 8-pin)
- [ ] XZERO: Described as "zero phase" not "stream zeros"
- [ ] Mode encoding: Uses D[31:28] format matching silicon doc
- [ ] All 80+ streamer symbols defined with correct values
- [ ] Frequency formula: `$8000_0000 × (rate / clock)`
- [ ] Common frequency values documented with +1 note

---

*Audit complete. Manual serves as authoritative reference for corrections.*
