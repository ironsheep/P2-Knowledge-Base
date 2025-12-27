# Hardware YAML Enhancement Sprint Plan
*Created: 2025-12-27*
*Updated: 2025-12-27 (User clarifications incorporated)*
*Purpose: Enable remote Claude to generate working code from YAML alone*

---

## Executive Summary

### The Problem
Our current hardware YAML files contain specifications (part numbers, dimensions, general descriptions) but **lack sufficient technical detail for code generation**. A remote Claude downloading these YAMLs cannot write functional code without guessing or searching elsewhere.

### The Solution
Enhance hardware YAMLs with:
1. **Complete pin mappings** - Header position → P2 pin chain (MANDATORY)
2. **Signal usage definitions** - How each signal is used
3. **Protocol constraints** - SPI clock limits, I2C speeds, timing requirements
4. **Circuit details** - Signal polarity, resistor values, current limits
5. **Smart Pin configurations** - P2-specific mode constants
6. **Working code patterns** - Initialization, read, write operations
7. **Resource pointers** - OBEX ID + URL, Quick Bytes URLs

### The Principle
- **Simpler boards**: Full technical extraction into YAML - self-sufficient for code generation
- **Complex boards**: Point to OBEX formal drivers - don't replicate complexity in YAML

### The Priority
- Build YAMLs for boards with complete sources
- Defer boards lacking source material until sources are available

---

## Critical YAML Requirements (User Specified)

### 1. Pin Mapping at Header Position (MANDATORY)
When a board is attached at Header A, the YAML must specify exactly which P2 pins are used:
```yaml
devices:
  led_0:
    header_pin: 1
    p2_pins_by_header:
      header_a: "P0"
      header_b: "P8"
      header_c: "P16"
      # ... all 8 headers
```

### 2. Signal Usage Definitions (MANDATORY)
How each signal is used:
```yaml
signal_usage:
  drive_type: "active_high"
  function: "LED control"
  direction: "output"
```

### 3. Protocol Constraints (MANDATORY where applicable)
For boards with fixed signaling (SPI, I2C):
```yaml
protocol_constraints:
  type: "SPI"
  max_clock_hz: 20000000
  clock_polarity: 0
  clock_phase: 0
  notes: "Don't exceed 20MHz to avoid overdriving"
```

### 4. Resource References (MANDATORY)
Always provide URLs when we've studied the source:
```yaml
resources:
  obex:
    id: 2869
    url: "https://obex.parallax.com/obex/p2es-control/"
  quick_bytes:
    - title: "LEDs – Beyond the Basics"
      url: "https://www.parallax.com/leds-beyond-the-basics/"
```

---

## Board Classification

### Category 1: Point to OBEX Only (Complex Drivers Required)

These boards have sophisticated drivers that shouldn't be replicated in YAML.

| Board | OBEX ID | URL | Driver | Author |
|-------|---------|-----|--------|--------|
| **64032** - HUB75 Adapter | 2850 | https://obex.parallax.com/obex/isp-hub75-matrix-driver/ | ISP Hub75 Matrix Driver | Iron Sheep |
| **BLDC Motor Board** | 2874 | https://obex.parallax.com/obex/isp-bldc-motor-control/ | ISP BLDC Motor Control | Iron Sheep |

**YAML Content**: Hardware identification, pin reference, pointer to OBEX driver. NO driver logic replication.

---

### Category 2: Extract to YAML (Self-Sufficient Documentation)

Full technical details captured in YAML for code generation.

| Board | OBEX | Quick Bytes | Source Status | Phase |
|-------|------|-------------|---------------|-------|
| **64006A** - Control (LEDs+Buttons) | 2869 ✅ | 2 | ✅ Complete | Phase 1 |
| **64006C** - LED Matrix (Charlieplex) | 2856 ✅ | 2 | ✅ Complete | Phase 1 |
| **64006D** - Servo Header | 2876 ✅ | 1 | ✅ Complete | Phase 1 |
| **64006G** - Goertzel (Touch Sensing) | ❌ | 1 ✅ | ⚠️ Fetch QB | Phase 1 |
| **64006H** - A/V Breakout | ❌ | 4 ✅ | ⚠️ Fetch QBs | Phase 1 |
| **P2-EC32MB** - Edge PSRAM Module | N/A | 0 | ✅ Complete | Phase 1 |

---

### Category 3: Awaiting User Examples

| Board | What's Needed | Status |
|-------|---------------|--------|
| **64006B** - Serial Host | USB host initialization, port control | ❌ Awaiting examples |
| **64006F** - Serial Device | USB device emulation, HID/CDC | ❌ Awaiting examples |

**64006E** (Mini Prototyping) - Pinout only, no code needed.

---

### Category 4: Deferred (Source Not Ingested)

| Board | What's Needed | Status |
|-------|---------------|--------|
| **64004** - HyperRAM Add-on | Product guide not ingested | ❌ Defer to later phase |

---

## Source Material Inventory

### Sources We Have (Ready to Extract)

#### OBEX Drivers
| OBEX ID | Name | Author | Location | Target |
|---------|------|--------|----------|--------|
| 2869 | P2ES Control | JonnyMac | `obex-projects/2869-P2ES_Control/` | 64006A |
| 2856 | P2ES Matrix | JonnyMac | `obex-projects/2856-P2ES_Matrix/` | 64006C |
| 2876 | Servo | JonnyMac | `obex-projects/2876-Servo/` | 64006D |
| 2867 | Accessory Board Buttons | Bryan Thomas | `obex-projects/2867-Accessory_Board_Buttons/` | Generic |
| PSRAM drivers | psram16drv, psram.spin2 | rogloh | `obex-projects/4162-MegaYume.../memstuff/` | P2-EC32MB |

#### Existing Knowledge Documents
| Document | Location |
|----------|----------|
| Circuit Knowledge | `ingestion/sources/p2-addon-board-circuit-knowledge.md` |
| Pin Mapping | `ingestion/sources/p2-board-pin-mapping-knowledge.md` |
| Extraction Audit | `ingestion/sources/p2-eval-add-on-boards/p2-eval-add-on-boards-complete-extraction-audit.md` |
| Quick Bytes Discovery | `ingestion/sources/quick-bytes-discovery-manifest.md` |

### Sources to Fetch (Quick Bytes - Add-on Board Relevant Only)

| Quick Byte | URL | Target |
|------------|-----|--------|
| Goertzel Operation with Ultrasonic Transducers | https://www.parallax.com/goertzel-operation-with-ultrasonic-transducers/ | 64006G |
| DVI/VGA Text Driver Demo | https://www.parallax.com/dvi-vga-text-driver-demo/ | 64006H |
| Video Hardware with Character Map Demo | https://www.parallax.com/video-hardware-character-map/ | 64006H |
| Simple Video Driver – Using Images | https://www.parallax.com/p2-simple-video-driver-using-images-intro-to-using-video-2-of-3/ | 64006H |
| Simple Sound Engine Demo | https://www.parallax.com/simple-sound-engine-demo/ | 64006H |
| LEDs – Beyond the Basics | https://www.parallax.com/leds-beyond-the-basics/ | 64006A |
| LED Matrix used as an I/O Test Utility | https://www.parallax.com/i-o-test-utility-with-led-matrix/ | 64006C |
| Multiple Servo Control (up to 64) Object | https://www.parallax.com/multiple-servo-control-up-to-64-object/ | 64006D |

### Sources Needed From User

| Board | Required | Notes |
|-------|----------|-------|
| **64006B** - Serial Host | USB host code examples | No OBEX, no Quick Bytes |
| **64006F** - Serial Device | USB device code examples | No OBEX, no Quick Bytes |

### Sources Not Yet Ingested (Deferred)

| Board | Required | Status |
|-------|----------|--------|
| **64004** - HyperRAM Add-on | Product guide PDF | User will locate; defer this phase |

---

## Enhanced YAML Schema

### Complete Example: Add-on Board with Protocol Constraints
```yaml
hardware_type: "addon_board"
part_number: "64006A"
p2kb_key: "p2kbHwAddonControlBoard"

basic_info:
  name: "P2 Eval Control Add-on Board"
  description: "Four push-buttons and four blue LEDs for user interface control"

specifications:
  electrical:
    supply_voltage: "3.3V from host"
    current_per_led_ma: 10
    total_current_ma: 40

# PIN MAPPING BY HEADER POSITION (MANDATORY)
pin_mapping:
  description: "Pin assignments when board is attached at each header position"
  header_a:
    base_pin: 0
    led_0: "P0"
    led_1: "P1"
    led_2: "P2"
    led_3: "P3"
    switch_0: "P4"
    switch_1: "P5"
    switch_2: "P6"
    switch_3: "P7"
  header_b:
    base_pin: 8
    led_0: "P8"
    # ... pattern continues

# SIGNAL USAGE DEFINITIONS (MANDATORY)
signals:
  leds:
    count: 4
    drive_type: "active_high"
    circuit: "P2_Pin → 330Ω → LED_Anode → Cathode → GND"
    resistor_ohms: 330
    current_ma: 10
    smart_pin_mode: "P_PWM_TRIANGLE | P_OE"
    
  switches:
    count: 4
    logic: "active_low"
    circuit: "3.3V → 10kΩ_pullup → P2_Pin → Switch → GND"
    pull_up_ohms: 10000
    debounce: "External capacitor provided"
    smart_pin_mode: "P_SCHMITT_A"

# PROTOCOL CONSTRAINTS (where applicable)
protocol_constraints:
  pwm:
    recommended_frequency_hz: 1000
    min_frequency_hz: 50
    max_frequency_hz: 100000
    notes: "Higher frequencies waste CPU cycles without visible benefit"

# CODE PATTERNS
code_patterns:
  spin2:
    init: |
      PUB init_control_board(base_pin) | i
        REPEAT i FROM 0 TO 3
          PINLOW(base_pin + i)        ' LEDs off
        REPEAT i FROM 4 TO 7
          PINFLOAT(base_pin + i)      ' Switches as inputs
    led_on: "PINHIGH(base_pin + led_num)"
    led_off: "PINLOW(base_pin + led_num)"
    switch_read: "NOT PINREAD(base_pin + 4 + switch_num)"

# RESOURCE REFERENCES (MANDATORY - with URLs)
resources:
  obex:
    id: 2869
    name: "P2ES Control"
    author: "Jon 'JonnyMac' McPhalen"
    url: "https://obex.parallax.com/obex/p2es-control/"
  quick_bytes:
    - title: "LEDs – Beyond the Basics"
      url: "https://www.parallax.com/leds-beyond-the-basics/"
```

### Complete Example: RAM Board with Protocol Constraints
```yaml
hardware_type: "edge_module"
part_number: "P2-EC32MB"
p2kb_key: "p2kbHwEdge32mbModule"

basic_info:
  name: "P2 Edge 32MB Module"
  description: "Enhanced P2 Edge module with 32MB PSRAM"

# PIN MAPPING (FIXED - not header-dependent)
pin_mapping:
  description: "Fixed pin assignments on Edge 32MB module"
  psram:
    data_bus_base: "P40"
    data_bus_width: 16
    clock_pin: "P56"
    chip_enable_pin: "P57"
    address_bits: 25

# PROTOCOL CONSTRAINTS (MANDATORY for memory interface)
protocol_constraints:
  psram:
    max_clock_hz: 160000000  # sysclk/2 at 320MHz
    supported_rates:
      - "sysclk/1 (fast mode)"
      - "sysclk/2 (standard)"
      - "sysclk/3"
      - "sysclk/4"
    max_cs_low_us: 8
    page_size_bytes: 4096
    total_capacity_bytes: 33554432  # 32MB

# CODE PATTERNS
code_patterns:
  spin2:
    init: |
      OBJ
        psram : "psram"
      PUB start()
        psram.start()
    read_burst: |
      psram.readBurst(hub_addr, ext_addr, byte_count)
    write_burst: |
      psram.writeBurst(hub_addr, ext_addr, byte_count)

# RESOURCE REFERENCES
resources:
  obex:
    id: 4162
    name: "MegaYume - Mega Drive Emulator (contains PSRAM drivers)"
    url: "https://obex.parallax.com/obex/megayume-mega-drive-emulator/"
    driver_files:
      - "psram.spin2"
      - "psram16drv.spin2"
```

---

## Execution Plan

### Phase 1: Boards With Complete Sources

#### Sprint 1: Source Gathering
| Task | Action | Status |
|------|--------|--------|
| 1.1 | Read OBEX 2869 (P2ES Control) | Ready |
| 1.2 | Read OBEX 2856 (P2ES Matrix) | Ready |
| 1.3 | Read OBEX 2876 (Servo) | Ready |
| 1.4 | Read PSRAM drivers (psram.spin2, psram16drv.spin2) | Ready |
| 1.5 | Fetch Goertzel Quick Byte | Web fetch |
| 1.6 | Fetch A/V Quick Bytes (4 pages) | Web fetch |
| 1.7 | Fetch remaining relevant Quick Bytes | Web fetch |

#### Sprint 2: Technical Extraction
| Task | Board | Source |
|------|-------|--------|
| 2.1 | 64006A - Control | OBEX 2869 + circuit docs |
| 2.2 | 64006C - LED Matrix | OBEX 2856 + circuit docs |
| 2.3 | 64006D - Servo Header | OBEX 2876 + circuit docs |
| 2.4 | 64006G - Goertzel | Quick Byte + circuit docs |
| 2.5 | 64006H - A/V Breakout | Quick Bytes + circuit docs |
| 2.6 | P2-EC32MB - PSRAM | PSRAM drivers |

#### Sprint 3: YAML Enhancement
| Task | Deliverable |
|------|-------------|
| 3.1 | Enhanced addon-control-board.yaml (64006A) |
| 3.2 | Enhanced addon-led-matrix.yaml (64006C) |
| 3.3 | Enhanced addon-servo-header.yaml (64006D) |
| 3.4 | Enhanced addon-goertzel-board.yaml (64006G) |
| 3.5 | Enhanced addon-av-breakout.yaml (64006H) |
| 3.6 | Enhanced edge-32mb-module.yaml (PSRAM) |
| 3.7 | Updated hub75_adapter.yaml (OBEX pointer) |

#### Sprint 4: Validation
| Task | Action |
|------|--------|
| 4.1 | Validate YAML syntax |
| 4.2 | Run cross-reference validation |
| 4.3 | Regenerate p2kb-index.json |
| 4.4 | Test download-on-demand queries |

---

### Phase 2: Awaiting User Examples

| Board | Waiting For | Action When Received |
|-------|-------------|----------------------|
| 64006B - Serial Host | USB host examples | Extract and build YAML |
| 64006F - Serial Device | USB device examples | Extract and build YAML |

---

### Phase 3: Deferred (Source Not Ingested)

| Board | Waiting For | Action When Available |
|-------|-------------|----------------------|
| 64004 - HyperRAM Add-on | Product guide ingestion | Full extraction sprint |

---

## Success Criteria

A remote Claude downloading any enhanced YAML can:

1. ✅ Identify exactly which P2 pins to use for the board's header position
2. ✅ Understand how each signal is used (polarity, function, direction)
3. ✅ Know protocol constraints (clock limits, timing requirements)
4. ✅ Know circuit details (resistor values, current limits)
5. ✅ Configure Smart Pins correctly
6. ✅ Write working initialization code
7. ✅ Write working read/write operations
8. ✅ Find OBEX driver via ID and URL if pre-built code desired
9. ✅ Find Quick Bytes tutorials via URL for learning

---

## Appendix A: Quick Bytes Discovery

See: `engineering/ingestion/sources/quick-bytes-discovery-manifest.md`

**Scope**: Add-on board relevant Quick Bytes only (not full ingestion)

| Board | Quick Bytes Available |
|-------|----------------------|
| 64006A (Control) | 2 |
| 64006C (Matrix) | 2 |
| 64006D (Servo) | 1 |
| 64006G (Goertzel) | 1 |
| 64006H (A/V) | 4 |

---

## Appendix B: OBEX Driver Inventory

| OBEX ID | Name | URL | Target |
|---------|------|-----|--------|
| 2850 | ISP Hub75 Matrix Driver | https://obex.parallax.com/obex/isp-hub75-matrix-driver/ | 64032 (point only) |
| 2856 | P2ES Matrix | https://obex.parallax.com/obex/p2es-matrix/ | 64006C (extract) |
| 2867 | Accessory Board Buttons | https://obex.parallax.com/obex/accessory-board-buttons/ | Generic (extract) |
| 2869 | P2ES Control | https://obex.parallax.com/obex/p2es-control/ | 64006A (extract) |
| 2874 | ISP BLDC Motor Control | https://obex.parallax.com/obex/isp-bldc-motor-control/ | BLDC (point only) |
| 2876 | Servo | https://obex.parallax.com/obex/servo/ | 64006D (extract) |
| 4162 | MegaYume (PSRAM drivers) | https://obex.parallax.com/obex/megayume-mega-drive-emulator/ | P2-EC32MB (extract) |

---

## Appendix C: RAM Board Status

| Board | Source Status | Phase |
|-------|---------------|-------|
| **P2-EC32MB** (PSRAM) | ✅ Complete - drivers and pin config available | Phase 1 |
| **64004** (HyperRAM) | ❌ Product guide not ingested | Deferred |

**P2-EC32MB Pin Configuration** (confirmed from source):
- Data bus: P40 (16-bit)
- Clock: P56
- Chip Enable: P57
- Address bits: 25 (32MB)
- Max CS low: 8 microseconds

---

*Plan finalized with user clarifications. Ready for Phase 1 execution.*
