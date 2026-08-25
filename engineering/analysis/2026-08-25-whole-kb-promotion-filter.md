# The whole-KB promotion filter — belonging as a disposition

**Task «#298» · 2026-08-25 · Plan §7 (decision D6, whole-KB scope)**

`deliverables/ai/P2/README.md` says the set is "optimized for AI code generation." Nothing
enforced that. This pass applies one test to every quantitative block in the shipped KB and to
every block the sprint's two purges removed, and records a disposition with a reason for each, so
that «#299» (architecture/language/guides/app-notes) and «#307» (hardware) can execute without
re-deciding.

---

## The test

> **Can this block change the code an agent emits?**

The calibration is the one in the task body. `instruction_to_pin_timing` giving `clock_cycles: 3`
and naming the instructions it applies to is **ACTIONABLE** — an agent can act on it. A
propagation delay of `typ: "3.5 ns"` at 25 °C is not: at 160 MHz one clock is 6.25 ns, so the
figure is below a single clock and no generated source can respond to it. It is not wrong. It is
not usable, and it displaces what is.

For every block below, the reason **names the concrete way generated code would differ** — a pin
number, a constant, a sequence, a bound, or a branch. Where no such difference could be named, the
block is not actionable, however technical it looks.

### Three dispositions

1. **ACTIONABLE** — it can change emitted code. Keep it, or let it return, cited.
2. **CORRECT BUT NOT ACTIONABLE** — true, but it belongs in the ingestion tree, not the shipped set.
3. **UNSOURCED** — should not have survived the purge. Routed back, never repopulated as-is.

### Four sub-rules, stated so they were applied consistently

- **M — mixed blocks.** The disposition unit is the top-level YAML key, and many blocks mix an
  actionable pin map with a non-actionable mounting-hole diameter. A block is
  CORRECT-BUT-NOT-ACTIONABLE only when **no part of it** can change emitted code. Any actionable
  part makes the whole block ACTIONABLE, because removing it would destroy that part. Mixed blocks
  are marked in their reason so a later pass can split them.
- **H — hardware.** Board-level facts **pass**: pin maps, what is wired where, module memory sizes,
  rates and timing bounds. A block describing only supply rails, connectors, mechanical parts,
  packaging, purchase or marketing does **not** — with one exception: a rail whose **enable is
  under software control** (the `addon-serial-host` 5 V enables at offsets 1 and 5) is ACTIONABLE,
  because the enable is an emitted pin write.
- **P — presence before removal.** A block ruled CORRECT-BUT-NOT-ACTIONABLE **must already exist in
  the ingestion tree before it leaves the KB**. Where it does not, it is **not deleted** — it stays,
  with the reason stated. See *Retained, not removed* below.
- **A — apparatus.** Provenance blocks, cross-reference indexes and `aliases` are neither claims nor
  code-changing, but they are load-bearing: the shipped-YAML-self-sufficiency rule and the P2KB
  findability mechanism both depend on them. They are recorded as CORRECT-BUT-NOT-ACTIONABLE and
  explicitly **RETAINED**. This is the one place the three-disposition scheme did not fit; see
  *Sharpening* at the end.

🔴 **Every disposition below is a judgement made by reading the block.** No script produced one.
Scripts were used only to enumerate blocks, check ingestion-tree presence, and count — and every
table below was generated from the measured block list, so no row can have been invented or dropped.

---

## Population 1 — what survived the purge

**114 quantitative blocks in 63 files** — 84 Tier 2 (wholly-uncited files) plus 30 that were
already cited. Measured with the sourcing gate's own parser, so the population is exactly the one
the gate sees.

### 1a. The 84 Tier-2 blocks

Distribution measured at entry: `hardware/` 39 · `language/` 22 · `architecture/` 18 ·
`community/` 4 · `guides/` 1 = **84**. (Confirms the dispatch's C1; the task body's 91 was stale.)

**Dispositions: 68 ACTIONABLE · 16 CORRECT-BUT-NOT-ACTIONABLE · 0 UNSOURCED**

| File (under `deliverables/ai/P2/`) | Block | Disposition | Reason |
|---|---|---|---|
| `architecture/decomposition/first-contact-procedure.yaml` | `procedure` | **ACTIONABLE** | The 9-step routine decides the cog map and object set an agent emits - how many cogs launch, which cog owns which bus, whether a protocol goes to a smart pin or a software loop. |
| `architecture/decomposition/rate-adaptation.yaml` | `how_it_cuts` | **ACTIONABLE** | choice_rule (every sample -> buffer; freshest only -> slot) and the one-bus-many-cadences resolution emit different objects. |
| `architecture/decomposition/rate-adaptation.yaml` | `summary` | **ACTIONABLE** | Names the buffer-vs-latest-wins-slot choice; that choice is a different data structure in emitted code. |
| `architecture/decomposition/spatial-computing.yaml` | `smells` | **ACTIONABLE** | Each smell's detectable_signature triggers a re-cut - a funnel cog removed, a lock replaced by a FIFO, a bit-banged protocol moved to a smart pin. |
| `architecture/decomposition/worked-derivation-robot-dog.yaml` | `derivation_steps` | **ACTIONABLE** | Produces a concrete cog map plus DAT-singleton vs VAR-instance transport choice - directly the object shape emitted. |
| `architecture/decomposition/worked-derivation-robot-dog.yaml` | `the_machine` | **ACTIONABLE** | The worked input the derivation consumes; its device/cadence mix is what makes step 5's cooperative-task answer reproducible. |
| `architecture/decomposition/worked-derivation-streaming-pipeline.yaml` | `derivation_steps` | **ACTIONABLE** | Emits a named 8-cog allocation, a frame pool + typed FIFOs, and per-consumer decimation ratios. |
| `architecture/decomposition/worked-derivation-streaming-pipeline.yaml` | `the_machine` | **ACTIONABLE** | The dual worked input; its cross-cog shared bus is what forces the resident-broker answer. |
| `architecture/smart-pins/smart-pin-01000-pwm-triangle.yaml` | `code_examples` | **ACTIONABLE** | The block IS emitted code - mode word, XVAL $0200_0001, YVAL, pinstart sequence and the PASM2 equivalent. |
| `architecture/smart-pins/smart-pin-01001-pwm-sawtooth.yaml` | `code_examples` | **ACTIONABLE** | Same - P_PWM_SAWTOOTH mode word and the exact WXPIN/WYPIN operands. |
| `architecture/smart-pins/smart-pin-01010-pwm-smps.yaml` | `code_examples` | **ACTIONABLE** | Emits the SMPS mode composition (P_PWM_SMPS | P_OE | P_MINUS1_A | P_PLUS1_B) and the comparator setup on adjacent pins. |
| `architecture/smart-pins/smart-pin-01111-count-highs-optional-dec.yaml` | `notes` | **ACTIONABLE** | States the 32-bit accumulator's overflow bound - an agent must bound the window or handle wrap. |
| `architecture/smart-pins/smart-pin-10000-time-a-states.yaml` | `detailed_description` | **ACTIONABLE** | Z saturates at $80000000; that is the guard/branch an agent emits after RDPIN. |
| `architecture/smart-pins/smart-pin-10001-time-a-highs.yaml` | `common_applications` | **ACTIONABLE** | Routes a servo-pulse / ultrasonic-echo task to mode %10001 - it changes which mode constant appears in generated code. |
| `architecture/smart-pins/smart-pin-10001-time-a-highs.yaml` | `detailed_description` | **ACTIONABLE** | Same saturation bound, plus 'IN raised on high-to-low only' which sets the poll condition. |
| `architecture/smart-pins/smart-pin-10010-time-x-a-events.yaml` | `detailed_description` | **ACTIONABLE** | Y[2] selects event-timing vs timeout and Y[1:0] the edge type - both are emitted WYPIN operand bits. |
| `architecture/smart-pins/smart-pin-10011-count-time-x-periods.yaml` | `detailed_description` | **ACTIONABLE** | A-to-B period accumulation over X periods; Y[1:0] edge selection is an emitted operand. |
| `architecture/streamer/nco-timing.yaml` | `video_rates` | **ACTIONABLE** | Precomputed SETXFRQ words per video mode per sysclk - copied verbatim into generated source. |
| `community/obex/objects/4012.yaml` | `object_metadata` | **ACTIONABLE** | The OBEX discovery record p2kb_obex_find/get serve; capability domain+leaf and the description decide which object an agent pulls in, which changes the OBJ line and its API. |
| `community/obex/objects/4070.yaml` | `object_metadata` | **ACTIONABLE** | Same. (Its 3 'quantities' are the instrument reading 'ISO/IEC 14443 A' as amperes - see F-348.) |
| `community/obex/objects/4727.yaml` | `object_metadata` | **ACTIONABLE** | Same; the 1.5/12 Mbps + 80-320 MHz clkfreq range is the applicability test an agent applies before selecting it. |
| `community/obex/objects/4858.yaml` | `object_metadata` | **ACTIONABLE** | Same; 3 contiguous pins per channel is a pin-allocation constraint on generated code. |
| `guides/spin2-getting-started.yaml` | `core_block_types` | **ACTIONABLE** | The block skeleton (CON/OBJ/VAR/DAT/PUB/PRI) and the required _clkfreq are the literal shape of emitted Spin2. |
| `hardware/addon-av-breakout.yaml` | `audio_capabilities` | **ACTIONABLE** | Names offsets 6/7 for L/R and offset 5 for the mic ADC - emitted pin assignments. |
| `hardware/addon-av-breakout.yaml` | `signal_map` | **ACTIONABLE** | Offsets 0-7 map to VGA HSync/RGB/VSync, mic and L/R audio - these become base+N pin numbers in generated code. |
| `hardware/addon-av-breakout.yaml` | `specifications` | **ACTIONABLE** | io_pins_used: 8 and the compatible-host list fix the pin group; the physical sub-map is not actionable but does not travel alone. |
| `hardware/addon-control-board.yaml` | `aliases` | **ACTIONABLE** | The P2KB findability mechanism harvests aliases; without them this board's signal map is unreachable by name. |
| `hardware/addon-control-board.yaml` | `availability` | **CORRECT BUT NOT ACTIONABLE** | Vendor, part-lookup string and bundle SKU. No pin, constant, sequence, bound or branch. |
| `hardware/addon-control-board.yaml` | `description` | **ACTIONABLE** | 470 ohm series + active-high on both LEDs and switches -> an agent emits pinhigh() to light and a weak-low drive to read. |
| `hardware/addon-control-board.yaml` | `part_number` | **ACTIONABLE** | Board identity is the retrieval key that selects this pin map over another board's. |
| `hardware/addon-control-board.yaml` | `signal_map` | **ACTIONABLE** | Offsets, directions, the P_LOW_15K + PINLOW read idiom and the ~20 ms debounce constant - all emitted. |
| `hardware/addon-control-board.yaml` | `specifications` | **ACTIONABLE** | io_pins_used: 8 fixes the group; mechanical sub-map rides along. |
| `hardware/addon-digital-video-out.yaml` | `advantages` | **CORRECT BUT NOT ACTIONABLE** | Marketing bullets; every technical fact in them is stated actionably elsewhere in the same file. |
| `hardware/addon-digital-video-out.yaml` | `description` | **ACTIONABLE** | Eight pins carry TMDS clock + 3 data lanes as differential pairs driven by the streamer - fixes the pin pairing and streamer mode. |
| `hardware/addon-digital-video-out.yaml` | `specifications` | **ACTIONABLE** | io_pins_used: 8 fixes the group. |
| `hardware/addon-digital-video-out.yaml` | `unused_connector_signals` | **CORRECT BUT NOT ACTIONABLE** | Pads deliberately NOT connected to any P2 pin, plus a solder-bridge instruction. No generated code can reach them. |
| `hardware/addon-led-matrix.yaml` | `advantages` | **CORRECT BUT NOT ACTIONABLE** | Bullets restating the description; no independent code-changing content. |
| `hardware/addon-led-matrix.yaml` | `description` | **ACTIONABLE** | The Charlieplex rule - drive one pin HIGH, one LOW, both INPUT to extinguish, one LED at a time, multiplex above ~50 Hz - IS the emitted loop. |
| `hardware/addon-led-matrix.yaml` | `specifications` | **ACTIONABLE** | io_pins_used: 8 fixes the group. |
| `hardware/addon-microsd.yaml` | `power_signals` | **CORRECT BUT NOT ACTIONABLE** | Supply rails only, no software enable. Nothing in generated code changes because VIO3V3 powers the card. |
| `hardware/addon-mini-prototyping.yaml` | `advantages` | **CORRECT BUT NOT ACTIONABLE** | Bullets; restates description and prototyping_grid. |
| `hardware/addon-mini-prototyping.yaml` | `description` | **ACTIONABLE** | States the eight header pins are uncommitted - an agent must take the base pin as a parameter and must not assume a signal map. |
| `hardware/addon-mini-prototyping.yaml` | `power_rails` | **CORRECT BUT NOT ACTIONABLE** | Breadboard supply rails and silk markings; no software enable. |
| `hardware/addon-mini-prototyping.yaml` | `prototyping_grid` | **CORRECT BUT NOT ACTIONABLE** | Hole grid, silk conventions and trace-cutting - assembly guidance, not code. |
| `hardware/addon-mini-prototyping.yaml` | `specifications` | **ACTIONABLE** | io_pins_used: 8 fixes the group. |
| `hardware/addon-wx-adapter.yaml` | `power_signals` | **CORRECT BUT NOT ACTIONABLE** | Two supply rails, no software enable. |
| `hardware/hardware-compatibility-matrix.yaml` | `addon_board_host_compatibility` | **ACTIONABLE** | pins_used per part number, the 8-pin group vs 16-pin dual-header split, and the P56-P63 programming-header note - all change pin constants. |
| `hardware/hardware-compatibility-matrix.yaml` | `incompatibilities` | **ACTIONABLE** | 'Multiple add-ons use the same P0-P7; use different header positions' changes the base-pin constant an agent emits. |
| `hardware/hardware-compatibility-matrix.yaml` | `optimal_configurations` | **CORRECT BUT NOT ACTIONABLE** | Shopping lists plus 'rationale' prose. No code-changing content. |
| `hardware/hardware-compatibility-matrix.yaml` | `performance_considerations` | **ACTIONABLE** | The 50 Hz flicker minimum is the refresh constant in a Charlieplex loop; the >180 MHz pin switching figure bounds a bit-banged clock. |
| `hardware/hardware-compatibility-matrix.yaml` | `physical_stacking_constraints` | **CORRECT BUT NOT ACTIONABLE** | Mounting holes, standoffs, modules-per-edge-position. Purely mechanical. |
| `hardware/hardware-compatibility-matrix.yaml` | `power_compatibility` | **CORRECT BUT NOT ACTIONABLE** | Supply sizing and per-board current budgets - a BOM/PSU decision, not a code decision. |
| `hardware/p1_rom_font_character_set.yaml` | `character_categories` | **ACTIONABLE** | Character codes are byte constants an agent emits to render text, schematic and waveform glyphs. |
| `hardware/p2-hardware-feature-comparison.yaml` | `addon_boards` | **ACTIONABLE** | pins_required, LED/switch counts, matrix geometry and the 470 ohm series value are all emitted constants. |
| `hardware/p2-hardware-feature-comparison.yaml` | `compatibility_matrix` | **ACTIONABLE** | pin_allocation names concrete pin ranges. (Its 'Up to 2 add-on boards' / two-header claim is wrong - the #64000 has eight; filed F-348.) |
| `hardware/p2-hardware-feature-comparison.yaml` | `development_boards` | **ACTIONABLE** | Crystal frequency, pin counts and regulation per board. (Three fabricated peripherals trimmed here this pass - see F-348.) |
| `hardware/p2-hardware-feature-comparison.yaml` | `edge_modules` | **ACTIONABLE** | Crystal frequency sets _xtlfreq; PSRAM presence decides whether a PSRAM driver is emitted at all. |
| `hardware/p2-hardware-feature-comparison.yaml` | `feature_matrix` | **ACTIONABLE** | Hub RAM 512KB, 64 smart pins, 16MB flash / 32MB PSRAM - the memory budget an agent allocates against. |
| `hardware/p2-hardware-feature-comparison.yaml` | `selection_criteria` | **CORRECT BUT NOT ACTIONABLE** | Cost tiers, experience levels and purchase rationale. |
| `hardware/p2-hardware-selection-guide.yaml` | `application_specific_guides` | **CORRECT BUT NOT ACTIONABLE** | Curriculum plans, investment totals and week counts. |
| `hardware/p2-hardware-selection-guide.yaml` | `compatibility_considerations` | **CORRECT BUT NOT ACTIONABLE** | PSU sizing, programmer choice and board dimensions. |
| `hardware/p2-hardware-selection-guide.yaml` | `decision_tree` | **CORRECT BUT NOT ACTIONABLE** | A buying decision tree with dollar estimates; the only technical fact (PSRAM size) is stated actionably in p2-hardware-feature-comparison.yaml. |
| `language/pasm2/asmclk.yaml` | `expansion_details` | **ACTIONABLE** | The literal HUBSET/WAITX/HUBSET sequence ASMCLK expands to - emitted verbatim when hand-rolling clock start. |
| `language/pasm2/hubset.yaml` | `clock_configuration` | **ACTIONABLE** | The clock-mode bit fields ARE the operand an agent computes and emits. |
| `language/pasm2/hubset.yaml` | `safe_clock_switching` | **ACTIONABLE** | The three-step configure/wait/switch sequence with its RDLONG/QDIV/GETQX/WAITX body. |
| `language/spin2/concepts/timing_operations.yaml` | `anti_patterns` | **ACTIONABLE** | Wrong/correct pairs that flip which of two idioms is emitted. |
| `language/spin2/concepts/timing_operations.yaml` | `description` | **ACTIONABLE** | Names the counter/delay/measurement API set an agent picks from. |
| `language/spin2/concepts/timing_operations.yaml` | `method_selection` | **ACTIONABLE** | Decides GETCT vs GETMS vs GETSEC - the documented fix for a real SD-driver overflow bug. |
| `language/spin2/concepts/timing_operations.yaml` | `minimum_resolution` | **ACTIONABLE** | Minimum practical delay per clock frequency - bounds whether WAITUS or inline WAITX is emitted. |
| `language/spin2/concepts/timing_operations.yaml` | `patterns` | **ACTIONABLE** | Nine complete emitted code patterns (periodic, timeout, debounce, soft PWM, multi-timer...). |
| `language/spin2/concepts/timing_operations.yaml` | `system_counter` | **ACTIONABLE** | The rollover table bounds every GETCT deadline an agent computes. |
| `language/spin2/concepts/timing_operations.yaml` | `time_conversions` | **ACTIONABLE** | The conversion formulas and the MULDIV64 substitution are emitted expressions. |
| `language/spin2/constants/special-configuration-symbols.yaml` | `clock_anti_patterns` | **ACTIONABLE** | Names combinations that fail to compile - directly prevents emitted code that does not build. |
| `language/spin2/constants/special-configuration-symbols.yaml` | `clock_configuration` | **ACTIONABLE** | _CLKFREQ/_XTLFREQ/_XINFREQ/_ERRFREQ/_RCFAST/_RCSLOW with their legal ranges - the CON block an agent writes. |
| `language/spin2/constants/special-configuration-symbols.yaml` | `clock_configuration_examples` | **ACTIONABLE** | Five complete CON blocks, emitted verbatim. |
| `language/spin2/constants/special-configuration-symbols.yaml` | `clock_configuration_rules` | **ACTIONABLE** | The combination rules decide which symbols appear together in the emitted CON block. |
| `language/spin2/constants/special-configuration-symbols.yaml` | `debug_output_control` | **ACTIONABLE** | DEBUG_MASK/DELAY/LOG_SIZE/DISABLE/TIMESTAMP are CON symbols an agent emits, with a version gate on DEBUG_MASK. |
| `language/spin2/methods/clkset.yaml` | `timing` | **ACTIONABLE** | The PLL settle delay an agent must emit between CLKSET and first use. |
| `language/spin2/methods/waitct.yaml` | `notes` | **ACTIONABLE** | Wrap handling and 1-clock resolution decide whether WAITCT or WAITMS is emitted. (Its wrap figure is quoted at 80 MHz while the rest of the KB uses 200 MHz - consistency nit, filed.) |
| `language/spin2/patterns/applications/single_communication.yaml` | `notes` | **ACTIONABLE** | Steers the emitted timeout to the GETMS form and names where the rule lives. |
| `language/spin2/system-variables/clkfreq.yaml` | `anti_patterns` | **ACTIONABLE** | waitx(clkfreq/1000) versus a hardcoded count - two different emitted lines. |
| `language/spin2/system-variables/clkmode.yaml` | `bit_fields` | **ACTIONABLE** | The CLKMODE word layout an agent decodes or constructs. |
| `language/spin2/system-variables/clkmode.yaml` | `clock_source_modes` | **ACTIONABLE** | SS field values and their frequencies - emitted operand bits. |
| `language/spin2/system-variables/clkmode.yaml` | `notes` | **ACTIONABLE** | Hub address $00040 for the PASM2 RDLONG, and the PLL-lock wait before switching. |

### 1b. The 30 already-cited quantitative blocks

**Dispositions: 23 ACTIONABLE · 5 CORRECT-BUT-NOT-ACTIONABLE · 2 UNSOURCED**

| File (under `deliverables/ai/P2/`) | Block | Disposition | Reason |
|---|---|---|---|
| `application-notes/p2an003-dac-analog-signal-generation.yaml` | `provenance` | **CORRECT BUT NOT ACTIONABLE** | Citation apparatus - RETAINED, see the apparatus note. Not code-changing, but the KB is its own home for provenance. |
| `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml` | `key_parameters` | **ACTIONABLE** | Mode constants, routing modifiers, the muldiv64 forms and the gate-window formula - the recipe an agent emits. |
| `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml` | `provenance` | **CORRECT BUT NOT ACTIONABLE** | Citation apparatus - RETAINED. |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `boot_pattern_table` | **ACTIONABLE** | Pin states select the boot path and its 60 s / 100 ms window - determines the pull configuration a design emits and the host-side wait. |
| `architecture/boot-rom/spi-flash-boot.yaml` | `phase_2_post_load_state` | **ACTIONABLE** | The loader's entry contract: CS low, mid-stream at $400, RCFAST, SCK=sysclk/2, and the WAITX #3 alignment pad. |
| `architecture/clock_system.yaml` | `clock_sources` | **ACTIONABLE** | RCFAST 20-30 MHz bounds any boot-time delay; the XI DC-200 MHz limit and PLL 320 MHz max bound an emitted clock config. |
| `architecture/cog.yaml` | `performance` | **ACTIONABLE** | The instruction-timing table is the cycle budget behind every WAITX value and inner-loop shape. |
| `architecture/cordic.yaml` | `performance` | **ACTIONABLE** | 55-clock latency and 8-clock issue interval set the pipelining depth of an emitted CORDIC loop. |
| `architecture/io_pin_timing.yaml` | `absolute_maximum_ratings` | **ACTIONABLE** | +/-30 mA per pin sizes an LED series resistor; +/-10 mA diode limit drives the 5 V series-resistor value. |
| `architecture/io_pin_timing.yaml` | `input_voltage_and_protection` | **ACTIONABLE** | The >=1 kohm series-resistor recipe for reading a 5 V signal is a concrete component value. |
| `architecture/io_pin_timing.yaml` | `related_topics` | **CORRECT BUT NOT ACTIONABLE** | Cross-reference index - RETAINED as apparatus. |
| `architecture/pin-drive-configuration.yaml` | `drive_ladder` | **ACTIONABLE** | The eight P_HIGH_*/P_LOW_* constants and their bit patterns - emitted WRPIN operands. |
| `architecture/pin-drive-configuration.yaml` | `idioms` | **ACTIONABLE** | weak_high/weak_low are complete emitted routines, hardware-verified (EF-063/EF-064). |
| `architecture/pin-power-domains.yaml` | `evidence` | **CORRECT BUT NOT ACTIONABLE** | Source list - RETAINED as apparatus for the 4-pin/8-pin grouping. |
| `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` | `registers` | **ACTIONABLE** | X/Y/Z register layouts are the exact WXPIN/WYPIN operands and RDPIN status decode. |
| `architecture/xbyte_engine.yaml` | `performance` | **ACTIONABLE** | 6-clock overhead and the 8-clock minimum loop are the budget an emitted bytecode interpreter is designed against. |
| `community/quick-bytes/five-buttons-on-one-pin.yaml` | `quick_byte` | **ACTIONABLE** | Discovery record for a reusable object; capability domain+leaf and related_boards route an agent to the object and its pin map. |
| `community/quick-bytes/leds-beyond-the-basics.yaml` | `quick_byte` | **ACTIONABLE** | Same. |
| `guides/pasm2-getting-started.yaml` | `timing_considerations` | **ACTIONABLE** | Instruction and hub-access clock counts - the budget behind emitted loop timing. |
| `hardware/addon-hd-audio.yaml` | `adc_board` | **ACTIONABLE** | Signal map offsets, I2C address $10 / bytes $20-$21, 400 kHz and the register range - emitted directly by a driver. |
| `hardware/addon-rtc.yaml` | `pin_mode_tip` | **ACTIONABLE** | 3.3 kohm pull-up in I2C output mode versus 150 kohm in input mode - two different emitted WRPIN modes on one pin. |
| `hardware/addon-rtc.yaml` | `resources` | **CORRECT BUT NOT ACTIONABLE** | Datasheet and product-page pointers - RETAINED as apparatus. |
| `hardware/addon-rtc.yaml` | `rtc_chip` | **ACTIONABLE** | I2C address $68 / $D0 / $D1, the 00h-13h register map, BCD encoding and the $58 software reset - all emitted. |
| `hardware/edge-32mb-module.yaml` | `protocol_constraints` | **ACTIONABLE** | PSRAM 133 MHz ceiling, the 8 us CS-low limit, the burst-size formula and the input-delay table are driver constants. |
| `language/pasm2/concepts/basic-io.yaml` | `hardware_specifications` | **UNSOURCED** | REMOVED this pass. 150mA per pin contradicts the datasheet's +/-30 mA absolute max, and the VIL 0.8 / VIH 2.0 / VOL 0.4 / VOH 2.4 pairs are 5 V-TTL boilerplate absent from the P2 datasheet. Cited only by the word 'datasheet' inside 'Check datasheet for package limits'. |
| `language/pasm2/getxacc.yaml` | `goertzel_usage` | **ACTIONABLE** | SINC1-vs-SINC2 choice, power-of-two sample counts and the 256-MHz-not-250 clock rule change the emitted setup. |
| `language/pasm2/setxfrq.yaml` | `frequency_formula` | **ACTIONABLE** | The $8000_0000 multiplier is the exact constant in the emitted expression. |
| `language/spin2/concepts/basic-io.yaml` | `hardware_specifications` | **UNSOURCED** | REMOVED this pass. Byte-identical twin of the PASM2 block above; same contradiction, same false-negative citation. |
| `language/spin2/patterns/implementation/spin2_cooperative_tasking.yaml` | `description` | **ACTIONABLE** | The {Spin2_v47} directive requirement is a literal first line of the emitted file; without it taskspin/tasknext do not compile. |
| `language/spin2/symbols/spin2-builtin-symbols-complete.yaml` | `spin2_builtin_symbols` | **ACTIONABLE** | 1224 symbol values and bit patterns - the constants an agent emits. |

### Where the boundary actually fell in Population 1

The 21 CORRECT-BUT-NOT-ACTIONABLE rulings are not evenly spread — 16 of them are in `hardware/`,
and they concentrate in three files and one shape:

- **`p2-hardware-selection-guide.yaml` is a buying guide, entire.** All three of its blocks are
  purchase decision trees with dollar estimates, curriculum week counts and `educational_rating`.
  Nothing in it names a pin, a constant or a bound. This is the cleanest case in the KB.
- **`hardware-compatibility-matrix.yaml` splits three-three.** `physical_stacking_constraints`
  (mounting), `power_compatibility` (PSU sizing) and `optimal_configurations` (shopping lists) fail;
  `addon_board_host_compatibility` (pins_used per board), `performance_considerations` (the 50 Hz
  flicker minimum) and `incompatibilities` (the P0-P7 conflict rule) pass. Same file, opposite sides.
- **`advantages:` blocks fail as a class.** Three of them (`addon-digital-video-out`,
  `addon-led-matrix`, `addon-mini-prototyping`) are marketing bullets whose every technical fact is
  already stated actionably elsewhere in the same file.

**The two boundary calls worth naming, because both could have gone the other way:**

1. **`p1_rom_font_character_set.yaml character_categories` → ACTIONABLE.** A 256-entry font table
   looks like reference data. It is not: the character codes are byte constants an agent emits to
   draw text, schematic symbols and waveform diagrams on a P2 text display. Code 189 + code 190 is
   *how you draw a resistor*. The named difference is a literal byte in a DAT block.
2. **`hardware/addon-microsd.yaml power_signals` → CORRECT BUT NOT ACTIONABLE.** This one *is* a
   "what is wired where" fact on a hardware board, which the rule says passes. It still fails,
   because nothing an agent emits changes based on VIO3V3 powering the card — there is no software
   enable. Sub-rule H exists to make that distinction survivable rather than case-by-case, and the
   contrast is `addon-serial-host`, where the 5 V rail *is* software-enabled at two named offsets
   and therefore passes.

### Retained, not removed — and why

**No Population-1 CORRECT-BUT-NOT-ACTIONABLE block was removed by this task.** Removing them is
`hardware/`-tree work and belongs to «#307». Two things are handed over with them:

- **Ingestion-tree presence is confirmed for the add-on board mechanical/pad content.** e.g. the
  mounting data behind `physical_stacking_constraints` and the four `specifications.physical`
  sub-maps lives at
  `engineering/ingestion/sources/p2-eval-add-on-boards/complete-p2-eval-add-on-boards-reference.md:36`;
  the HDMI unused-pad list at
  `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-digital-video-out-64006d.md:25-26`;
  the prototyping grid, white-box/dash convention and ground strip at
  `.../boards/addon-mini-prototyping-64006e.md:12-16`. Those are safe to remove after a per-block check.
- 🔴 **The buying-guide content has NO ingestion home.** `grep -rln '\$150-200\|educational_rating\|cost_tier'`
  over `engineering/ingestion/sources/` returns **nothing**. Under sub-rule P these blocks —
  `p2-hardware-selection-guide.yaml` (all three) and `p2-hardware-feature-comparison.yaml
  selection_criteria` — **do not get deleted**. They are authored-here content with no upstream. They
  must be written to the ingestion tree first, or they stay. **«#307» must not simply delete them.**

---

## Population 2 — the 119 repopulation candidates

Reconstructed from git and cross-checked against the register, block by block:
**60 («#293», `15c84de5`) + 48 + 11 («#294», `c733a223`) = 119.** Every row below corresponds to a
verified top-level key that was present before the purge and is absent now.

> **F-347's open count discrepancy resolves at 60.** The register recorded "60 reconstructed vs 59
> reported." All 60 were re-verified individually against `15c84de5^`: each is a real top-level key
> present pre-removal and absent from the current file. **No row is a no-op**; the executor's 59 was
> an undercount, and the reconstruction stands. Nothing was deleted to reconcile.
>
> **F-334's record is complete at 59, but the naive reconstruction says 63.** Four extra `-key:`
> lines in `c733a223` — `edge-breadboard-carrier feature_class`, `edge-mini-breakout size_advantage`,
> `edge-standard-breakout pin_utilization`, `p2-eval-board alternative_to` — are **end-of-file
> newline no-ops**: each has a matching `+key:` with identical content in the same commit. They are
> **not** removals and are **not** repopulation candidates. Anyone re-deriving this list from git
> must exclude re-added keys or they will hand «#307» four phantom rows.

### 2a. F-347 — «#293», 60 blocks / 25 files → owner **«#299»**

**Dispositions: 46 ACTIONABLE · 1 CORRECT-BUT-NOT-ACTIONABLE · 13 UNSOURCED**

| File | Block | Disposition | Reason / instruction to «#299» |
|---|---|---|---|
| `application-notes/p2an001-single-pin-instrumentation-adc.yaml` | `gotchas` | **ACTIONABLE** | Pitfalls that change emitted code: keep a measurement inside one 4-pin silicon domain; X[3:0] power-of-two only in SAMPLING mode; stay at a legal clock. |
| `application-notes/p2an002-cordic-for-real-work.yaml` | `gotchas` | **ACTIONABLE** | QMUL/QDIV/QFRAC/QSQRT unsigned vs QVECTOR/QROTATE signed; keep hub access out of both CORDIC loops - both change the emitted loop body. Empirically grounded. |
| `application-notes/p2an003-dac-analog-signal-generation.yaml` | `key_parameters` | **ACTIONABLE** | P_DAC_* output configs, the V = code/65536 * Vfs math, the 256-clock dither period and the DDS phase-increment formula. |
| `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml` | `gotchas` | **ACTIONABLE** | P_B_A_INPUT does not exist; P_LOW_FLOAT is mandatory for R1; `sar 2` normalizes a detented encoder. Each is a concrete emitted line. |
| `architecture/boot-rom/_index.yaml` | `boot_paths_summary` | **ACTIONABLE** | Per-path pin assignments and the 100 ms / 60 s windows. |
| `architecture/boot-rom/_index.yaml` | `boot_timing` | **ACTIONABLE** | The ~5 ms reset-to-decision budget bounds a host-side programmer wait and any boot-time stub. |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `boot_time_clock_state` | **ACTIONABLE** | Boot-time code must be calibrated for RCFAST 20-30 MHz, not the user's eventual clock - changes every emitted delay in a loader. |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `pin_triple_duty` | **ACTIONABLE** | Custom boards must wire P58-P61 to SPI flash and provide boot-time pull-ups - a concrete design constraint. |
| `architecture/boot-rom/spi-flash-boot.yaml` | `boot_pattern_trigger` | **ACTIONABLE** | Pattern-to-behavior mapping for the flash-priority patterns. |
| `architecture/click_module_integration.yaml` | `best_practices` | **ACTIONABLE** | 'Always use offset constants, never hardcode pins' and 'make base pin a runtime parameter' are the emitted code's shape. |
| `architecture/clock_system.yaml` | `anti_patterns` | **ACTIONABLE** | Wrong/correct pairs that flip the emitted CON block and the post-HUBSET wait. |
| `architecture/clock_system.yaml` | `clock_modes` | **ACTIONABLE** | CC and SS field values. |
| `architecture/clock_system.yaml` | `clock_specifications` | **ACTIONABLE** | 180 MHz recommended / 350 MHz absolute bound an emitted _clkfreq. |
| `architecture/clock_system.yaml` | `configuration_constants` | **ACTIONABLE** | Return de-duplicated against special-configuration-symbols.yaml clock_configuration, which survived and carries the same content. |
| `architecture/clock_system.yaml` | `configuration_rules` | **ACTIONABLE** | Same de-dup; note this copy carries one extra rule (DEBUG with no clock defaults to 20 MHz) the survivor lacks. |
| `architecture/clock_system.yaml` | `hubset_configuration` | **ACTIONABLE** | The clock-mode operand layout, emitted directly. |
| `architecture/clock_system.yaml` | `pll_system` | **ACTIONABLE** | VCO range, divider/multiplier ranges and the post-divider value list are needed to compute a HUBSET word by hand. NOTE: its max_overclock 350 MHz must be reconciled with the surviving cited clock_sources note. |
| `architecture/clock_system.yaml` | `stabilization_timing` | **ACTIONABLE** | The settle delay an agent emits. *** CONFLICT: this block says pll_lock ~10 microseconds; clkset.yaml, clkmode.yaml and hubset.yaml (all surviving) say ~10 ms. Three orders of magnitude, in a wait that ships. Resolve before returning - filed F-348. *** |
| `architecture/io_pin_timing.yaml` | `best_practices` | **CORRECT BUT NOT ACTIONABLE** | Generic PCB layout advice (match trace lengths, 22-33 ohm source termination). True of any fast CMOS part, changes no generated source. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `clock_relationships` | **UNSOURCED** | 5-8 / 7-10 / 6-9 ns path totals with no source, same fabrication family. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `compensation_techniques` | **UNSOURCED** | 150 ps/inch FR4, 0.3%/10C and 2%/100mV coefficients - none sourced, and the last two are the fabricated timing model's derivatives. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `description` | **UNSOURCED** | Asserts configurable slew rate. 'slew' appears zero times across the Silicon Doc, Spin2 sources and smart-pins catalog (F-327). DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `drive_strength_configurations` | **UNSOURCED** | F-327 verbatim. The real ladder is the eight rungs in pin-drive-configuration.yaml drive_ladder, which is cited. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `input_characteristics` | **UNSOURCED** | VIL 0.8 / VIH 2.0 is 5 V-TTL boilerplate; the datasheet states Vih ratiometric (Vxxyy*0.3/0.5/0.7). Schmitt 1.65/1.35/300 mV unsourced. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `protocol_timing_examples` | **UNSOURCED** | Generic SPI/I2C/SD protocol lore presented as P2 pin timing. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `slew_rate_control` | **UNSOURCED** | A whole feature the P2 does not have. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `special_timing_modes` | **UNSOURCED** | ~100 MHz sync-serial, ~10 Mbps UART, ~50 MHz DDR - no source states any of them. DO NOT RETURN. |
| `architecture/io_pin_timing.yaml` | `timing_specifications` | **UNSOURCED** | F-327 core: propagation/rise/fall tables keyed to a 1.5/3/15/30/75/150 mA ladder that does not exist. DO NOT RETURN. |
| `architecture/pin-power-domains.yaml` | `board_power_grouping` | **ACTIONABLE** | V00..V56 to pin-range mapping, 300 mA per group, 30 mA per pin - the budget an agent allocates against. |
| `architecture/pin-power-domains.yaml` | `description` | **ACTIONABLE** | HIGH PRIORITY. Silicon 4-pin VIO/GIO groups vs board 8-pin LDO groups decides which pins an agent groups for an absolute ADC measurement. The surviving cited `evidence` block already carries both sources. |
| `architecture/serial_loader.yaml` | `boot_sequence` | **ACTIONABLE** | P62/P63 assignment, the 100 ms / 60 s windows and the hub $00000 entry point. |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `operation` | **ACTIONABLE** | The Fclock/256 tone at -48 dB and 'max 2 transitions per 256 clocks' decide whether this mode or %00010 is emitted for a given signal. |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pin_behavior` | **ACTIONABLE** | Reset state and 'OUT=1 enables ADC for load measurement' are emitted configuration bits. |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pwm_characteristics` | **ACTIONABLE** | X[7:0]=0 and the 256-clock minimum period are hard constraints on the emitted WXPIN operand. |
| `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` | `detailed_description` | **ACTIONABLE** | Even pin = DM, odd pin = DP - fixes the pin pair an agent assigns. Return alongside the surviving cited `registers` block. |
| `architecture/smart_pin_patterns.yaml` | `notes` | **ACTIONABLE** | Config-ordering rule for streamer/smart-pin SPI, and the GETMS-over-GETCT steering for client code. |
| `architecture/smart_pins.yaml` | `electrical_limits` | **ACTIONABLE** | A safety-critical routing note - 'the P2 is 3.3 V I/O, NOT natively 5 V tolerant' plus the pointer to the cited absolute_maximum_ratings. |
| `architecture/smart_pins.yaml` | `input_routing` | **ACTIONABLE** | A/B input source selection and the FILT0-3 debounce times are emitted mode-word choices. Verify the four filter values against the Silicon Doc on return. |
| `architecture/smart_pins.yaml` | `related_components` | **ACTIONABLE** | Cross-reference index (apparatus). Returning it restores the navigation edge to timing_operations.yaml. Crossrefs still validate without it, so this is restoration, not repair. |
| `guides/pasm2-getting-started.yaml` | `file_structure` | **ACTIONABLE** | HIGH PRIORITY. The minimal PASM2 program skeleton - CON/DAT/ORG/FIT $1F0, 496 longs, ORG vs ORGH - is emitted verbatim. |
| `language/pasm2/concepts/basic-io.yaml` | `control_registers` | **ACTIONABLE** | $1FA-$1FF register addresses and their bit-to-pin mapping - emitted directly by PASM2. |
| `language/pasm2/concepts/basic-io.yaml` | `drive_strength_configuration` | **UNSOURCED** | F-327 ladder verbatim (1.5/3/15/30/75/150 mA with invented impedances). Superseded by pin-drive-configuration.yaml drive_ladder. DO NOT RETURN. |
| `language/pasm2/concepts/basic-io.yaml` | `internal_pull_resistors` | **ACTIONABLE** | RETURN CORRECTED. P_HIGH_/P_LOW_1K5/15K/150K/1MA are real v55 constants, but this block's sequence uses DIRL for 'input with pull-up', which EF-063/EF-064 disprove - the weak drive is inactive with DIR=0. Reconcile against pin-drive-configuration.yaml idioms before returning. |
| `language/pasm2/concepts/basic-io.yaml` | `pin_architecture` | **ACTIONABLE** | RETURN WITHOUT the `drive_strength: 1.5mA to 150mA` line (F-327 fabrication). Pin count, P0-P63 range, DIRA/DIRB split and the real 1.5k/15k/150k pull values all stand. |
| `language/pasm2/concepts/basic-io.yaml` | `timing_considerations` | **UNSOURCED** | 'pin_propagation: 3-7ns' is the io_pin_timing fabrication family. The 2-clock instruction figure is already carried, cited, in cog.yaml and pasm2-getting-started.yaml. DO NOT RETURN. |
| `language/pasm2/concepts/streamer_smartpin_control.yaml` | `protocol_client_code_note` | **ACTIONABLE** | Steers client-code timeouts to GETMS; names where the full rule lives. |
| `language/pasm2/setxfrq.yaml` | `common_values` | **ACTIONABLE** | Precomputed SETXFRQ words. Cross-check against nco-timing.yaml video_rates on return - both carry $0CE3_BCD3 for 25.175 MHz at 250 MHz. |
| `language/spin2/concepts/basic-io.yaml` | `control_registers` | **ACTIONABLE** | Register-to-pin mapping for the Spin2 side. |
| `language/spin2/concepts/basic-io.yaml` | `drive_strength_configuration` | **UNSOURCED** | F-327 ladder verbatim. DO NOT RETURN. |
| `language/spin2/concepts/basic-io.yaml` | `internal_pull_resistors` | **ACTIONABLE** | RETURN CORRECTED - same EF-063/EF-064 conflict; PINSTART then PINFLOAT is the disproven shape. |
| `language/spin2/concepts/basic-io.yaml` | `pin_architecture` | **ACTIONABLE** | RETURN WITHOUT the `drive_strength` line, exactly as the PASM2 twin. |
| `language/spin2/concepts/basic-io.yaml` | `timing_considerations` | **UNSOURCED** | Same 3-7 ns fabrication. DO NOT RETURN. |
| `language/spin2/debug-commands/pc_key.yaml` | `description` | **ACTIONABLE** | The ~100 ms host latch window sets the poll rate an agent emits. |
| `language/spin2/debug-commands/pc_key.yaml` | `usage_rules` | **ACTIONABLE** | HIGH VALUE. The backtick rule and 'must be LAST' prevent a silent runtime failure that compiles clean. |
| `language/spin2/methods/getct.yaml` | `pitfalls` | **ACTIONABLE** | The 2^31 overflow rule. Return as a cross-reference to timing_operations.yaml method_selection, which survived carrying the same rule. |
| `language/spin2/methods/waitms.yaml` | `limitations` | **ACTIONABLE** | 1 ms resolution and blocking behaviour decide WAITMS vs WAITCT. |
| `language/spin2/methods/waitms.yaml` | `notes` | **ACTIONABLE** | The ~4294 s ceiling and the 'under 1 ms use WAITUS' rule pick which call is emitted. |
| `language/spin2/methods/waitus.yaml` | `clock_frequency_impact` | **ACTIONABLE** | Clocks-per-microsecond per frequency decides WAITUS versus an inline WAITX. |
| `language/spin2/methods/waitus.yaml` | `limitations` | **ACTIONABLE** | 1 us floor and degradation at low clocks. |
| `language/spin2/methods/waitus.yaml` | `notes` | **ACTIONABLE** | Resolution floor and the 'over 1000 us use WAITMS' rule. |

### 2b. F-334 first record — «#294», 48 blocks / 16 files → owner **«#307»**

**Dispositions: 33 ACTIONABLE · 15 CORRECT-BUT-NOT-ACTIONABLE · 0 UNSOURCED**

| File | Block | Disposition | Reason / instruction to «#307» |
|---|---|---|---|
| `hardware/addon-goertzel-touch.yaml` | `specifications` | **ACTIONABLE** | io_pins_used: 8 and the host list fix the pin group. |
| `hardware/addon-hd-audio.yaml` | `dac_board` | **ACTIONABLE** | HIGH PRIORITY. Signal-map offsets, the four P_DAC_* base modes, and the parallel-pin impedance divider (base/N) are emitted verbatim. |
| `hardware/addon-hd-audio.yaml` | `description` | **ACTIONABLE** | 4-channel / 32-bit / 192 kHz ADC and a DAC built on smart-pin DAC modes - decides which driver shape is emitted. |
| `hardware/addon-hd-audio.yaml` | `set_contents` | **CORRECT BUT NOT ACTIONABLE** | Kit contents; both facts restated actionably in description and dac_board. |
| `hardware/addon-hd-audio.yaml` | `use_cases` | **CORRECT BUT NOT ACTIONABLE** | Application-domain bullets. |
| `hardware/addon-hyperram-hyperflash.yaml` | `configuration` | **ACTIONABLE** | The RES shunt position decides whether an emitted driver must assert IO+15 to release reset. |
| `hardware/addon-hyperram-hyperflash.yaml` | `specifications` | **ACTIONABLE** | 16 MB PSRAM / 32 MB flash sizes and the 100 MHz max clock are driver constants. |
| `hardware/addon-motor-driver.yaml` | `current_sense` | **ACTIONABLE** | 150 mV per amp is the emitted conversion constant. |
| `hardware/addon-motor-driver.yaml` | `power_signals` | **CORRECT BUT NOT ACTIONABLE** | On-board boost regulators; no software enable. |
| `hardware/addon-motor-driver.yaml` | `protection` | **CORRECT BUT NOT ACTIONABLE** | Hardware protections that operate without software participation. |
| `hardware/addon-motor-driver.yaml` | `pwm_control` | **ACTIONABLE** | Active-high logic, the 250 ns minimum deadtime and the 20 kHz typical / 50 kHz max are the emitted PWM configuration. |
| `hardware/addon-motor-driver.yaml` | `signal_map` | **ACTIONABLE** | Sixteen offsets mapping PWM high/low per phase, Hall inputs and current/voltage sense - every one becomes a pin constant. |
| `hardware/addon-motor-driver.yaml` | `specifications` | **ACTIONABLE** | io_pins_used: 16 and the 3.3 V TTL thresholds; ratings ride along. |
| `hardware/addon-rtc.yaml` | `description` | **ACTIONABLE** | PCF8523 over I2C - selects the driver and its address space (both in the surviving cited rtc_chip block). |
| `hardware/addon-rtc.yaml` | `power_signals` | **CORRECT BUT NOT ACTIONABLE** | Two supply rails, no software enable. |
| `hardware/addon-rtc.yaml` | `specifications` | **CORRECT BUT NOT ACTIONABLE** | Battery chemistry, mechanical dimensions and shipping classification. |
| `hardware/addon-serial-device.yaml` | `description` | **ACTIONABLE** | 1 kOhm LED series and assert-high polarity - an agent emits pinhigh() to light. |
| `hardware/addon-serial-device.yaml` | `signal_map` | **ACTIONABLE** | LEDs at offsets 0/1/6/7 and USB D-/D+ at 2/3 and 4/5 - the even/odd pin pair the USB smart-pin mode requires. |
| `hardware/addon-serial-host.yaml` | `signal_map` | **ACTIONABLE** | Offsets 1 and 5 are software 5 V enables - literal emitted pin writes; D-/D+ pairs at 2/3 and 6/7. |
| `hardware/addon-serial-host.yaml` | `usb_host_capabilities` | **ACTIONABLE** | The enable-control offsets and power sequence are an emitted sequence. |
| `hardware/addon-wx-wifi.yaml` | `part_variants` | **CORRECT BUT NOT ACTIONABLE** | SKU variants. |
| `hardware/addon-wx-wifi.yaml` | `pin_descriptions` | **ACTIONABLE** | /PGM, DO/DI, /RES and /CTS mapping is the emitted UART plus reset control (and the 4x /PGM pulse to force AP+STA). |
| `hardware/addon-wx-wifi.yaml` | `specifications` | **CORRECT BUT NOT ACTIONABLE** | Electrical ratings and mechanical form factors. |
| `hardware/edge-32mb-module.yaml` | `boot_modes` | **ACTIONABLE** | DIP settings to boot behaviour, including the 60 s / 100 ms windows. |
| `hardware/edge-32mb-module.yaml` | `development_workflow` | **ACTIONABLE** | Names the emitted API: psram.start(), psram.read(), psram.write() and the cog-mailbox interface for multi-cog access. |
| `hardware/edge-32mb-module.yaml` | `limitations` | **ACTIONABLE** | P40-P57 unavailable, one cog consumed by the PSRAM driver, P24-P31 switching restriction - all constrain an emitted design. |
| `hardware/edge-32mb-module.yaml` | `pin_mapping` | **ACTIONABLE** | HIGHEST PRIORITY IN THE TREE. P40-P57 PSRAM, P58-P61 flash/SD, P62/P63 serial, per-group VIO - this block decides which pin numbers appear in generated code. 744 -> 321 lines when it went. |
| `hardware/edge-32mb-module.yaml` | `specifications` | **ACTIONABLE** | HIGH PRIORITY. PSRAM bank organization, 133 MHz chip ceiling, the 8 us CS-low limit and hub/cog/LUT sizes are all driver constants. |
| `hardware/edge-breadboard-carrier.yaml` | `power_specifications` | **CORRECT BUT NOT ACTIONABLE** | Input options and current budget prose. |
| `hardware/edge-breadboard-carrier.yaml` | `specialized_features` | **CORRECT BUT NOT ACTIONABLE** | Breadboard tie points, servo header count and power rails; the pin assignment is explicitly 'configurable', so it names nothing. |
| `hardware/edge-breadboard-carrier.yaml` | `specifications` | **CORRECT BUT NOT ACTIONABLE** | Dimensions, weight (TBD) and supply options. |
| `hardware/edge-mini-breakout.yaml` | `connectivity` | **ACTIONABLE** | '40 accessible pins' is the pin budget an agent must respect on this carrier, and add-on incompatibility rules out the #64006 pin maps. |
| `hardware/edge-mini-breakout.yaml` | `power_management` | **CORRECT BUT NOT ACTIONABLE** | Regulation and distribution prose. |
| `hardware/edge-mini-breakout.yaml` | `specifications` | **CORRECT BUT NOT ACTIONABLE** | Dimensions and supply. |
| `hardware/edge-standard-breakout.yaml` | `connectivity` | **ACTIONABLE** | 'All 64 pins accessible' is the complementary pin budget. |
| `hardware/edge-standard-breakout.yaml` | `power_management` | **CORRECT BUT NOT ACTIONABLE** | Regulation and distribution prose. |
| `hardware/edge-standard-breakout.yaml` | `specifications` | **CORRECT BUT NOT ACTIONABLE** | Dimensions and supply. |
| `hardware/edge-standard-module.yaml` | `boot_modes` | **ACTIONABLE** | DIP settings to boot behaviour. |
| `hardware/edge-standard-module.yaml` | `pin_mapping` | **ACTIONABLE** | HIGHEST PRIORITY. P0-P55 free and LEDs on P56/P57 - DIFFERENT PINS from the 32MB module. Getting this wrong puts an LED write on a PSRAM data line. 582 -> 270 lines when it went. |
| `hardware/edge-standard-module.yaml` | `specifications` | **ACTIONABLE** | HIGH PRIORITY. Same driver-constant role as the 32MB module, with psram: null as the discriminator. |
| `hardware/hub75_adapter.yaml` | `description` | **ACTIONABLE** | 3.3 V to 5 V level shifting for HUB75 - decides that no P2-side level handling is emitted. |
| `hardware/hub75_adapter.yaml` | `notes` | **ACTIONABLE** | Max 3 chains and the 1/8, 1/16, 1/32 scan patterns are emitted configuration. |
| `hardware/hub75_adapter.yaml` | `software_features` | **ACTIONABLE** | The driver API, measured refresh rates and the clock/latch/OE pulse widths are emitted timing constants. |
| `hardware/hub75_adapter.yaml` | `specifications` | **ACTIONABLE** | 40 MHz max / 35 MHz reliable and 13 ns propagation bound the emitted bit-bang clock. |
| `hardware/p2-eval-board.yaml` | `specifications` | **ACTIONABLE** | RETURN CORRECTED from the repaired capture, NOT verbatim: Rev C not Rev D; 180 MHz recommended not 320 MHz; 16 MB W25Q128JVSIM; 3.55in x 3.55in; -40 to +85 C; two micro-USB (500 mA / 2000 mA), absolute max 5.5 VDC. See F-328(b). |
| `hardware/programming-prop-plug.yaml` | `description` | **ACTIONABLE** | The 3 Mbaud ceiling and 3.3 V / 5 V target compatibility bound an emitted baud constant. |
| `hardware/programming-prop-plug.yaml` | `reset_option` | **ACTIONABLE** | DTR-vs-RTS reset selection and the ~20 us pulse are the download handshake a host-side tool emits. |
| `hardware/programming-prop-plug.yaml` | `specifications` | **ACTIONABLE** | The 300 baud to 3 Mbps range bounds emitted serial configuration. |

### 2c. F-334 second record — «#294» finishing, 11 blocks / 6 files

**Dispositions: 2 ACTIONABLE · 9 CORRECT-BUT-NOT-ACTIONABLE · 0 UNSOURCED**

| File | Block | Disposition | Reason / instruction |
|---|---|---|---|
| `hardware/addon-hyperram-hyperflash.yaml` | `host_note` | **CORRECT BUT NOT ACTIONABLE** | A jumper-position note; the board draws no 5 V, so nothing in generated code changes. |
| `hardware/addon-serial-device.yaml` | `rev_b_5v_note` | **CORRECT BUT NOT ACTIONABLE** | A shunt-jumper note for one board revision. |
| `hardware/addon-serial-device.yaml` | `specifications` | **CORRECT BUT NOT ACTIONABLE** | 3.3 V supply plus mechanical dimensions. |
| `hardware/addon-serial-host.yaml` | `description` | **CORRECT BUT NOT ACTIONABLE** | Prose about the load switch and the 5 V requirement; the software-controllable part is the enable pin, which lives in signal_map. |
| `hardware/addon-serial-host.yaml` | `development_workflow` | **ACTIONABLE** | 'Enable desired USB ports (set base+1 and/or base+5 high)' is an emitted pin-write sequence. |
| `hardware/addon-serial-host.yaml` | `limitations` | **CORRECT BUT NOT ACTIONABLE** | Supply and current limits; the one code-relevant item (uses all 8 pins) is in specifications/signal_map. |
| `hardware/addon-serial-host.yaml` | `power_requirements` | **CORRECT BUT NOT ACTIONABLE** | The same current budget restated; a PSU decision. |
| `hardware/addon-serial-host.yaml` | `specifications` | **CORRECT BUT NOT ACTIONABLE** | Current ratings and mechanical dimensions. |
| `hardware/edge-standard-module.yaml` | `revision_history` | **CORRECT BUT NOT ACTIONABLE** | Board revision history - VIN, current and switcher-frequency changes across Rev A-D. None reaches generated source. |
| `hardware/hub75_adapter.yaml` | `power_requirements` | **CORRECT BUT NOT ACTIONABLE** | External panel PSU sizing; explicitly never supplied through the P2 board. |
| `language/spin2/methods/getct.yaml` | `description` | **ACTIONABLE** | Owner is #299, not #307. The 32-bit wrap and 'use PASM2 GETCT D WC for the upper 32 bits' change emitted code. Its ~21 s figure is DERIVED (2^32/200 MHz) - return with a source or rewrite so it does not compute. |

### The thirteen that must never come back

All thirteen UNSOURCED rulings are one fabrication family, and **nine of them are a single file**:
`architecture/io_pin_timing.yaml`. This is F-327 — a drive ladder (1.5/3.0/15/30/75/150 mA with
invented impedances), a programmable slew rate the P2 does not have, and a propagation/rise/fall
timing model built on top of both. The remaining four are the same content copied into
`language/pasm2/concepts/basic-io.yaml` and `language/spin2/concepts/basic-io.yaml`
(`drive_strength_configuration` ×2, `timing_considerations` ×2, the latter carrying the same
fabricated `3-7ns` figure).

**The real ladder is the eight rungs in `architecture/pin-drive-configuration.yaml drive_ladder`,
which is cited to the datasheet Pin Mode Legend and survives.** That file's `no_other_rungs` key
states the rule explicitly: *"Any per-pin current or impedance figure beyond them is not in the
source."* Any repopulation that reintroduces a milliamp drive ladder is reintroducing F-327.

### Two conflicts that must be resolved *before* anything returns

🔴 **1. PLL lock time differs by three orders of magnitude across the KB.**
The removed `architecture/clock_system.yaml stabilization_timing` says `pll_lock: "~10 microseconds"`.
Three **surviving** blocks say milliseconds: `language/spin2/methods/clkset.yaml timing`
("~10-20ms for PLL lock"), `language/spin2/system-variables/clkmode.yaml notes` ("PLL must lock
before switching to PLL source (~10ms)") and `language/pasm2/hubset.yaml safe_clock_switching`
("Wait ~10ms for PLL lock"), and `language/pasm2/asmclk.yaml expansion_details` emits
`WAITX ##20_000_000/100` — a 10 ms wait at 20 MHz. This is a delay an agent **emits**. Returning
the µs figure without resolving it ships a contradiction into generated code. Filed as F-348.

🔴 **2. Two removed blocks teach a pull-resistor idiom that hardware disproves.**
`internal_pull_resistors` (both `basic-io.yaml` files) shows `DIRL #16 ' Use as input with pull-up`
and `PINSTART(...P_HIGH_15K...)` followed by `PINFLOAT(16)`. EF-063 and EF-064 — real silicon,
2026-08-20 — establish that the weak drive is **inactive** with DIR = 0; the surviving cited
`pin-drive-configuration.yaml idioms` states `dir: "1 -- required; with DIR = 0 the pin floats and
the drive is inactive"`. Both blocks are ruled ACTIONABLE because the constants are real, but they
must be **returned corrected**, reconciled against `idioms`, never verbatim.

### Highest-value returns, so «#299» and «#307» can order the work

| Rank | Block | Why it leads |
|---|---|---|
| 1 | `hardware/edge-32mb-module.yaml pin_mapping` | Decides which pin numbers appear in generated code. 744 → 321 lines when it went. |
| 2 | `hardware/edge-standard-module.yaml pin_mapping` | Same, and the pins **differ** from the 32MB module — LEDs on P56/P57, not P38/P39. Confusing them puts an LED write on a PSRAM data line. |
| 3 | `architecture/pin-power-domains.yaml description` + `board_power_grouping` | The silicon-4 vs board-8 grouping decides ADC measurement layout; the surviving cited `evidence` block already carries both sources. |
| 4 | `guides/pasm2-getting-started.yaml file_structure` | The minimal PASM2 program skeleton, emitted verbatim. |
| 5 | `hardware/addon-hd-audio.yaml dac_board` | P_DAC_* modes plus the parallel-pin impedance divider. |
| 6 | `language/spin2/debug-commands/pc_key.yaml usage_rules` | Prevents a silent runtime failure that compiles clean. |

---

## F-328(b) — the six items the sourcing gate structurally cannot see

These carry **no unit-bearing quantity**, so the gate never inspected them; two purges passed over
them. Read by ID from the register and each checked against the repaired capture
`engineering/ingestion/sources/p2-eval-board/complete-p2-eval-board-reference.md`.

| # | Item | Disposition | Evidence | Action |
|---|---|---|---|---|
| 1 | `built_in_peripherals.proto_area` | **UNSOURCED** | `grep -rn -i "prototyp\|breadboard"` over the repaired capture returns **zero hits**. The #64000 has no prototyping area. | **REMOVED** |
| 2 | `built_in_peripherals.switches.user_switches: "TBD quantity"` | **UNSOURCED** | Capture `:120` Reset Button and `:123` "**Four** dip switches: USB RES, FLASH, P59 △, P59 ▽". There are no user switches. | **REMOVED** |
| 3 | `built_in_peripherals.headers.connector_type: "Standard 0.1 inch headers"` | **UNSOURCED** | Capture `:35` "**eight I/O Pin Breakout Edge Headers** accommodate the 2×6 pass-through headers". The 0.1″ feature is the AUX power **pads** (`:115`). | **REMOVED** |
| 4 | `video_audio:` (`vga_support`/`hdmi_support`/`audio_output`) | **UNSOURCED** | `grep -rn -i "\bVGA\b\|HDMI\|resistor DAC\|audio"` returns **zero hits**. Fabricated whole. | **REMOVED** |
| 5 | `connectivity.programming` (USB-B/USB-C + Prop Plug #32201) | **UNSOURCED** | Capture `:59` "Serial over **micro-USB**", `:76` "Dual power inputs via **micro-USB** sockets". No USB-B, no USB-C, no Prop Plug, no #32201. | **REMOVED** |
| 6 | `expansion_ecosystem.individual_addons` | **ACTIONABLE — RETAINED** | **Not a fabrication.** It is a cross-reference roster, and its two questioned entries are sourced elsewhere: #64032 HUB75 has its own KB file (`hardware/hub75_adapter.yaml`, `part_number: 64032`), and #64008 MicroBUS appears in the ingestion tree (`sources/edge-mini-breakout/`, `sources/p2-microSD-addon/`). It routes an agent to a board's pin map. | **KEPT** |

**Item 6 is the one the dispatch expected to be fabricated and is not.** F-328 itself left it open
("they may be sourced elsewhere; that is the repopulation step's call") — that call is now made,
in favour of keeping it.

---

## Class-wide sweep: the F-328(b) fabrication class is not confined to one file

Sweeping the class, not the occurrence, found the **same invented eval-board peripherals in a
second file**: `hardware/p2-hardware-feature-comparison.yaml`, `development_boards.p2_eval_board`.

**Removed (fabricated — the board has none of them):** `audio_capability: "Stereo DAC output"` ·
`video_capability: "VGA output"` · `breadboard_area: "Large prototyping area"`.

**Retained but WRONG — filed for «#307», needs re-derivation, not deletion:**

| Key | Ships | Repaired capture says |
|---|---|---|
| `dimensions` | `127×89mm` | **3.55″ × 3.55″** (`:62`, `:260`) ≈ 90 × 90 mm |
| `usb_connectivity` | `USB-C programming + micro-USB serial` | **two micro-USB** (`:59`, `:76`); no USB-C |
| `addon_headers` | `Two 2x6 headers for add-on boards` | **eight** I/O breakout edge headers (`:35`, `:52`) |
| `flash_memory` | `16MB (with P2-EC)` | 16 MB is right; the #64000 has the P2 **soldered on-board** (`:124`), it is not an edge-module carrier |
| `compatibility_matrix.eval_board_addons` | `Up to 2 add-on boards` / `A-side (P32-P39) + B-side (P24-P31)` | eight headers in **8 groups of 8** covering all 64 pins (`:52`) |

---

## Removals executed by this task

**Ten items removed across four files** (two whole top-level blocks and eight sub-keys), each file preceded by a backup via `engineering/tools/backup-file.sh`
(`.backups/…20260825-082653` and `…20260825-082759`).

| File | What | Disposition | Preserved where |
|---|---|---|---|
| `language/pasm2/concepts/basic-io.yaml` | `hardware_specifications` (11 lines) | UNSOURCED | Correct facts already shipped, cited, in `architecture/io_pin_timing.yaml absolute_maximum_ratings`; source at `engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:2142` (±30 mA), `:2163` (Vih ratiometric), `:2172`–`:2178` (Vol/Voh) |
| `language/spin2/concepts/basic-io.yaml` | `hardware_specifications` (11 lines) | UNSOURCED | same |
| `hardware/p2-eval-board.yaml` | 5 × F-328(b) items | UNSOURCED | Nothing to preserve — none of it is in any source; the **true** replacements are in the repaired capture, cited in the F-328(b) table above |
| `hardware/p2-hardware-feature-comparison.yaml` | 3 fabricated eval-board peripherals | UNSOURCED | same |

Verified as pure deletions: `git diff --numstat` reports `0` insertions for all four YAML files, and a
parsed nested diff against `HEAD` shows exactly the two top-level blocks and eight sub-keys named
above removed — **no key added, no surviving value changed**.

**Why these two `hardware_specifications` blocks were removed rather than left for «#299».** They
shipped `max_current_per_pin: "150mA"` — **five times** the datasheet's `±30 mA` absolute maximum
per I/O pin, in the exact number an agent uses to size an LED series resistor — together with
`VIL_max 0.8V` / `VIH_min 2.0V` / `VOL_max 0.4V` / `VOH_min 2.4V`, which are 5 V-TTL boilerplate the
P2 datasheet does not contain (it states a single ratiometric `Vih` of `Vxxyy × 0.3/0.5/0.7`, and
Vol/Voh as millivolt **drops** at a stated current). They survived both purges through a citation
false negative: the gate judged the block cited because the word **"datasheet"** appears inside
`max_current_total: "Check datasheet for package limits"` — a **deferral**, not an attribution.
Every other block in the KB judged cited by an inline token names a real document. Nothing
`related:`/`see_also:` referenced `hardware_specifications`; `validate-crossref-keys.py` re-ran
clean after removal. Filed F-348. Repopulation, if any, is «#299»'s.

---

## Sharpening — for the skill-evolution buffer

"Belonging is a disposition" has no owning skill. This pass sharpened it in four places:

1. **The mixed-block rule (M) is the load-bearing one.** Without it, the filter is unusable in
   `hardware/`, where nearly every `specifications:` block pairs `io_pins_used: 8` with a
   mounting-hole diameter. "Any actionable part makes the block actionable" is what keeps the test
   non-destructive at the granularity the KB is actually written at.
2. **The three dispositions have no slot for *apparatus*.** Provenance blocks, cross-reference
   indexes and `aliases` are not claims and do not change emitted code, so the test says
   "not actionable" — and acting on that would strip the trust chain and break findability. Five
   Population-1 blocks landed here. A fourth disposition, **APPARATUS — retain unconditionally**,
   is the honest fix.
3. **Sub-rule P has a third branch nobody wrote down.** The task's error case assumes a
   not-actionable block either *is* in the ingestion tree (remove) or *should be written there
   first*. The buying-guide content is a third case: **authored-here content with no upstream at
   all**, which cannot be "returned" to an ingestion tree it never came from. The rule needs an
   explicit "stays, and say why" branch — which is what was applied.
4. **A purge keyed on missing citations is orthogonal to belonging, and to truth.** F-328(b) proved
   the first (six fabrications with no unit-bearing quantity sailed through two purges); the two
   `hardware_specifications` blocks proved the second (a *cited* block, contradicting its own named
   source by 5×). Neither is a gate defect the gate can fix alone — both need a read-and-decide pass.
   That is the argument for this test having an owner.
