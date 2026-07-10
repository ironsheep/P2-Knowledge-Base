# Fabrication-Audit Fan-Out — MASTER REGISTER (all 13 released docs)

**Sprint:** Fabrication Audit & Correctness Sweep — plan §5 fan-out (task #177)  
**Spec:** FABRICATION-AUDIT-FAN-OUT-SPEC.md v1.1.0  
**Generated:** 2026-07-10 — Batch 1 (narrative core, 12 docs) + Batch 2 (IOSP)  
**Scope note:** Assembly Part I covered by the pilot register; Assembly Part II/III (existing 100% per-entry audit) excluded.

> Candidate findings: each survived an independent adversarial refute-verify. **Pending human hand-check + class-wide sweep (§6/§7).** Per-doc detail in each doc's `audit/fanout-findings-2026-07-10.md`; PASM2 Part I in `pilot-part-i-findings-register-2026-07-09.md`.

## Cross-doc scorecard

| Doc | Claims | Survivors | Rejected |
|-----|-------:|----------:|---------:|
| IOSP User Guide | 2375 | 154 | 33 |
| Debug Window Manual | 939 | 97 | 26 |
| DeSilva PASM Tutorial | 648 | 63 | 7 |
| Streamer Guide | 323 | 8 | 2 |
| App Note P2AN001 | 78 | 6 | 4 |
| Getting Started | 95 | 4 | 2 |
| App Note P2AN002 | 70 | 4 | 2 |
| App Note P2AN004 | 39 | 3 | 0 |
| Architect's Guide | 125 | 1 | 5 |
| Assembly (front-matter only) | 32 | 1 | 1 |
| App Note P2AN003 | 92 | 1 | 2 |
| App Note P2AN005 | 69 | 1 | 0 |
| App Note P2AN006 | 49 | 0 | 0 |
| **TOTAL (13 docs)** | **4934** | **343** | **84** |

## Survivor breakdown
- By verdict: {'unverifiable': 59, 'misaligned': 276, 'fabricated': 6, 'yaml-wrong': 1, 'operator': 1}
- By confidence: {'low': 131, 'high': 81, 'medium': 131}

## Recurring defect classes across the whole set (survivors, ≥2) — the §6/§7 sweep work-list

| n | defect_class | docs touched |
|--:|--------------|--------------|
| 6 | cycle-count-vs-instruction-count | p2-pasm-desilva-style |
| 6 | pinfloat-disables-internal-pull | p2-io-and-smart-pins-user-guide |
| 5 | gio-used-as-signal-input | p2-io-and-smart-pins-user-guide |
| 4 | hub-loop-cycle-understatement | p2-pasm-desilva-style |
| 4 | packing-signedness-misattribution | p2-debug-window-manual |
| 4 | usb-pair-upper-pin-wrpin-omitted | p2-io-and-smart-pins-user-guide |
| 3 | invented-default-value | p2-debug-window-manual |
| 3 | color-format-rgb24-vs-named | p2-debug-window-manual |
| 3 | debug-window-range-mismatch | p2-debug-window-manual |
| 3 | nco-frequency-resolution-inverted | p2-io-and-smart-pins-user-guide |
| 3 | pasm-immediate-address-vs-value | p2-io-and-smart-pins-user-guide |
| 3 | smartpin-mode-constant-mismatch | p2-io-and-smart-pins-user-guide |
| 2 | false-chapter-backreference | p2-getting-started-guide |
| 2 | color-name-green-vs-lime | p2-debug-window-manual |
| 2 | term-default-pair3-color | p2-debug-window-manual |
| 2 | luma-hsv-x-variant-mischaracterized | p2-debug-window-manual |
| 2 | save-missing-filename-arg | p2-debug-window-manual |
| 2 | default-value-mismatch | p2-debug-window-manual |
| 2 | alt-modifier-semantics-wrong | p2-debug-window-manual |
| 2 | adc-pin-power-group-size-four-vs-eight | P2AN001 |
| 2 | cordic-precision-bits-unsourced | P2AN002 |
| 2 | c-flag-mode-meaning-fabrication | p2-io-and-smart-pins-user-guide |
| 2 | maximum-toggle-rate-not-maximum | p2-io-and-smart-pins-user-guide |
| 2 | y-count-range-off-by-one | p2-io-and-smart-pins-user-guide |
| 2 | nco-jitter-direction-inverted | p2-io-and-smart-pins-user-guide |
| 2 | frame-field-16bit-overflow | p2-io-and-smart-pins-user-guide |
| 2 | period-field-zero-unverified | p2-io-and-smart-pins-user-guide |
| 2 | bit-dac-nibbles-unset-no-output | p2-io-and-smart-pins-user-guide |
| 2 | invert-a-vs-invert-b | p2-io-and-smart-pins-user-guide |
| 2 | enob-vs-nominal-bits-reframing | p2-io-and-smart-pins-user-guide |
| 2 | gio-reference-used-as-signal-input | p2-io-and-smart-pins-user-guide |
| 2 | wrong-invert-constant-a-vs-in | p2-io-and-smart-pins-user-guide |
| 2 | dac-mode-dithering-overgeneralization | p2-io-and-smart-pins-user-guide |
| 2 | pick-one-orthogonal-fields | p2-io-and-smart-pins-user-guide |
| 2 | smartpin-mode-invalid-config | p2-io-and-smart-pins-user-guide |
| 2 | debug-diagnostic-wrong-register | p2-io-and-smart-pins-user-guide |
| 2 | sync-rx-x5-mode-mislabel | p2-io-and-smart-pins-user-guide |

## Priority set — HIGH-confidence fabricated/misaligned (hand-check first)

| Doc | Location | Verdict | Class | Claim |
|-----|----------|---------|-------|-------|
| p2-getting-started-guide | getting-started-body.md Ch3 §"Sh | misaligned | false-chapter-backrefere | the P2 gives you **locks** (the 16 hardware locks from Chapt |
| p2-streamer-programming-guide | Appendix D §"Corrupted Data from | misaligned | fifo-wrap-address-alignm | Buffer address aligned to 64-byte boundary for wrap mode |
| p2-pasm-desilva-style | Ch2 §Your Turn Experiment 2 'Par | misaligned | ptrb-not-a-user-paramete | rdlong delay, ptrb reads a per-cog 'delay' parameter passed  |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md, Ch.4 Co | misaligned | hub-immediate-bit-width | A bare #address only encodes 9 bits ... Always use ## for hu |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch5 Comm | misaligned | mul-16x16-mischaracteriz | MUL gives only low 32 bits; for the full 64-bit result you m |
| p2-pasm-desilva-style | opus-master/COMPLETE-OPUS-MASTER | misaligned | cordic-per-cog-fabricati | Each cog has its own CORDIC, but starting a new operation be |
| p2-pasm-desilva-style | opus-master/COMPLETE-OPUS-MASTER | misaligned | cordic-overwrite-vs-pipe | starting a new operation before retrieving your result overw |
| p2-pasm-desilva-style | Ch.8 §Reading Multiple Pins area | misaligned | testp-flag-polarity-inve | if_z jmp #sensor_low ' Jump if pin low (Z=1 when pin=0)  /   |
| p2-pasm-desilva-style | Ch.8 §Timing Is Everything, line | misaligned | sequential-instructions- | When you execute drvh #56 then drvl #57, 'Pin 56 goes high a |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.10 'L | misaligned | address-width-32-vs-20-b | jmp #\far_away — '\ forces a 32-bit absolute address' |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.10 'P | misaligned | alignl-8byte-vs-4byte-lo | 'Align branch targets to 8-byte boundaries' followed by 'ali |
| p2-pasm-desilva-style | Chapter 12 §The Hook, COMPLETE-O | misaligned | hub-loop-cycle-understat | Before optimization: 13 clocks (for the rdlong/add/wrlong/ad |
| p2-pasm-desilva-style | Chapter 12 §The Hook, COMPLETE-O | misaligned | cycle-count-vs-instructi | Almost twice as fast! (the 'after optimization' loop that me |
| p2-pasm-desilva-style | Chapter 12 §Hub Access Optimizat | misaligned | hub-alignment-timing-fab | Non-long-aligned hub access is slower and long-aligned acces |
| p2-pasm-desilva-style | Chapter 12 §The FIFO Fast Path,  | misaligned | hub-loop-cycle-understat | Traditional hub reading (rdlong ptra++ / add / djnz loop): ~ |
| p2-pasm-desilva-style | Chapter 12 §Real-World Example F | misaligned | hub-loop-cycle-understat | copy_better (rdlong ptra++ / wrlong ptrb++ / djnz) runs ~8 c |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.12 'U | misaligned | ptr-expression-scope-ove | ptra++ only works with hub-access instructions like RDLONG. |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.13 'C | misaligned | cog-ram-address-range-er | In 'mov value, $200', $200 is a cog RAM address (so it reads |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md §Ch13 'W | misaligned | cycle-count-wrong | 3-clock deterministic access via RDLUT / WRLUT |
| p2-pasm-desilva-style | §'ATN - Inter-Cog Events', COMPL | misaligned | cogatn-mask-width | The COGATN instruction takes an 8-bit mask where each bit co |
| p2-debug-window-manual | ch02-getting-started.md §The no- | misaligned | random-operator-single-v | the random-number generator — `GETRND` (or the `?` operator) |
| p2-debug-window-manual | ch03-term.md §A positioned dashb | misaligned | term-default-pair3-color | Selecting color pair 3 (code 7) in this example gives red 'H |
| p2-debug-window-manual | ch05-plot.md §The update model / | misaligned | precise-default-inverted | the window keeps sub-pixel precision (1/256 of a pixel) by d |
| p2-debug-window-manual | ch06-logic.md §Creating a LOGIC  | misaligned | worked-example-bit-mappi | a sample value of %1011 lights channel 0 (CLK) high, channel |
| p2-debug-window-manual | ch06-logic.md config-keyword tab | misaligned | logic-keyword-defaults-c | LINESIZE default 3, range 1–32 |
| p2-debug-window-manual | ch08-scope-xy.md §Creating a SCO | misaligned | dotsize-pixels-vs-half-p | DOTSIZE argument is in pixels and sets the dot diameter, ran |
| p2-debug-window-manual | ch13-packed-data.md §The ALT and | misaligned | alt-modifier-semantics-w | ALT — the host swaps adjacent same-width fields throughout t |
| p2-debug-window-manual | ch13-packed-data.md §Considerati | misaligned | alt-modifier-semantics-w | Use ALT only to swap adjacent same-width fields throughout t |
| p2-debug-window-manual | appendix-b-packed-data.md § Modi | misaligned | alt-modifier-reversal-mi | ALT: swap adjacent same-width fields ... not a reversal |
| p2-debug-window-manual | appendix-b-packed-data.md § Modi | misaligned | alt-modifier-scope-overs | ALT: swap ... fields throughout the container |
| P2AN001 | P2AN001.md §How It Works (in bri | misaligned | adc-pin-power-group-size | the P2 powers its I/O pins in isolated groups of four, and a |
| P2AN001 | P2AN001.md §Recipe 2, line 247 | misaligned | adc-pin-power-group-size | Those four are one complete 4-pin power group (32–35), so th |
| P2AN001 | P2AN001.md §Pitfalls & Notes, li | misaligned | pin-power-group-size | The P2 powers its I/O pins in isolated groups of four — pins |
| P2AN004 | P2AN004.md §Recipe R3, Hardware  | misaligned | filter-length-mismatch | If a turned knob jumps or counts backward, add `P_FILT1_AB`  |
| P2AN005 | P2AN005.md §Adapt It / Going Fur | misaligned | false-negative-capabilit | which would need a hardware mutex the P2 doesn't have |
| p2-io-and-smart-pins-user-guide | front-matter.md, Document Conven | misaligned | wrpin-mode-field-bit-pos | mode bits \| Bits [4:0] in WRPIN value selecting Smart Pin m |
| p2-io-and-smart-pins-user-guide | §1.10 Instruction Quick Referenc | misaligned | testp-both-flags-overcla | TESTP/TESTPN set both C and Z to the pin's input state. |
| p2-io-and-smart-pins-user-guide | §1.8 intro, line 986 | misaligned | alias-set-membership-und | Spin2 also accepts short-form aliases for the three most com |
| p2-io-and-smart-pins-user-guide | part-1-fundamentals/chapter-02-e | misaligned | edio-fields-misattribute | the muted fields (A/B input routing in bits [31:21] and the  |
| p2-io-and-smart-pins-user-guide | chapter-04-smart-pin-configurati | misaligned | spin2-method-existence-e | There is no direct Spin2 equivalent [to AKPIN]. Use RDPIN wi |
| p2-io-and-smart-pins-user-guide | §7.7 Example 4 (PASM2 Continuous | misaligned | dat-label-immediate-addr | The example configures smart pin 10: STEP_PIN is defined `ST |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-08-n | misaligned | integer-division-truncat | 65536 * 2 / 3 = 43691 (240 degree phase word). |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-09-p | misaligned | frame-field-16bit-overfl | Choose: Base period = 1, Frame period = 100,000  → PWM perio |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-09-p | misaligned | frame-field-16bit-overfl | frame := _clkfreq / (2 * freq_hz) ... WXPIN(PWM_PIN, 1 \| (f |
| p2-io-and-smart-pins-user-guide | §9.7 Example 4 (PASM2 High-Frequ | misaligned | pasm-immediate-label-add | PASM2 example configures pin 20 for 100 kHz PWM; PWM_PIN is  |
| p2-io-and-smart-pins-user-guide | chapter-10-dac-output.md §10.8 E | misaligned | qsin-parameter-name-erro | QSIN's third parameter is a "twist" (parameter list document |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-11-s | misaligned | rev-operand-off-by-one | value REV 8 reverses 8 bits for MSB-first SPI transmission |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-11-s | misaligned | pasm-rev-needs-shl-first | A bare `rev data` reverses the data bits for MSB-first sync  |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-11-s | misaligned | invert-a-vs-invert-b | To select negative (falling) clock edge for P_SYNC_TX, add P |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-11-s | misaligned | rev-operator-off-by-one | reversed := value REV 8   ' reverse the data bits for MSB-fi |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-11-s | misaligned | bit-count-off-by-one | or  x_val, #8   (setting X[4:0]=8 in an '8 data bits' async- |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-11-s | misaligned | pasm2-label-addr-as-imme | Example 4 configures/transmits on TX_PIN (pin 20) via dirl/w |
| p2-io-and-smart-pins-user-guide | part-2-output-modes/chapter-11-s | misaligned | fractional-baud-ignored- | Using X[15:10] fractional timing gives <0.001% error at 1152 |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | testp-wz-flag-polarity-i | After `testp #pin wz`, `if_z jmp #pin_low ' Branch if zero ( |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | pinfloat-disables-intern | Configuring `WRPIN(pin, P_HIGH_15K)` then `PINFLOAT(pin)` pr |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | pinfloat-disables-intern | `WRPIN(pin, P_LOW_15K)` then `PINFLOAT(pin)` produces an act |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | pinfloat-disables-intern | `WRPIN(pin, P_SCHMITT_A \| P_HIGH_15K)` then `PINFLOAT(pin)` |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | pinfloat-disables-intern | Unused-pin 'Option 2: Pull-down' via `WRPIN(unused_pin, P_LO |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | pinfloat-disables-intern | Unused-pin 'Option 3: Pull-up' via `WRPIN(unused_pin, P_HIGH |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | pinfloat-disables-intern | button_init configures `WRPIN(BUTTON_PIN, P_HIGH_15K) ' Inte |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-12-di | misaligned | pasm-immediate-address-v | Example 3 configures and polls BUTTON_PIN (pin 20); `mov pin |
| p2-io-and-smart-pins-user-guide | chapter-13-timing-measurement.md | misaligned | pasm-immediate-address-v | Example 3 ("PASM2 High-Speed Frequency Counter") configures/ |
| p2-io-and-smart-pins-user-guide | chapter-16-adc.md §16.6 multi_ad | misaligned | gio-used-as-signal-input | Configures 8 consecutive pins as ADC channels with P_ADC_GIO |
| p2-io-and-smart-pins-user-guide | chapter-16-adc.md §16.7 Example  | misaligned | gio-used-as-signal-input | An example titled 'Simple Potentiometer Reading' configures  |
| p2-io-and-smart-pins-user-guide | chapter-16-adc.md §16.7 Example  | misaligned | gio-used-as-signal-input | Configures AUDIO_PIN with P_ADC_GIO and captures a SINC2-fil |
| p2-io-and-smart-pins-user-guide | chapter-16-adc.md §16.7 Example  | misaligned | gio-used-as-signal-input | Frames P_ADC_GIO as a 'ground-referenced' pin-input mode fro |
| p2-io-and-smart-pins-user-guide | chapter-16-adc.md §16.7 Example  | misaligned | gio-used-as-signal-input | PASM2 example configures ADC_PIN with P_ADC_GIO, then event- |
| p2-io-and-smart-pins-user-guide | chapter-16-adc.md §16.7 Example  | misaligned | event-mode-rises-vs-high | Comment labels SETSE1 mode %001 as 'Event on IN high'. |
| p2-io-and-smart-pins-user-guide | §17.2 P_ASYNC_RX Operation, line | fabricated | async-stopbit-validation | The smart pin monitors for a high-to-low transition (start b |
| p2-io-and-smart-pins-user-guide | §17.3 MSB-First Reception, line  | misaligned | spin2-rev-operand-off-by | value := value REV 32  ' Reverse all 32 bits (then value :=  |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-17-se | misaligned | wrong-invert-constant-a- | For RS-232 with external level shifter, invert the received  |
| p2-io-and-smart-pins-user-guide | part-3-input-modes/chapter-17-se | misaligned | wrong-invert-constant-a- | P_INVERT_IN inverts the (received serial) input, for RS-232. |
| p2-io-and-smart-pins-user-guide | chapter-18-repository.md §18.8 K | misaligned | in-flag-repository-vs-sa | **All modes**: IN raised when sample period completes |
| p2-io-and-smart-pins-user-guide | appendix-d §Input Mode Compariso | misaligned | smartpin-mode-constant-m | P_COUNT_HIGHS measures 'Gated edges' and is used as a 'Freq  |
| p2-io-and-smart-pins-user-guide | appendix-d §Counting Mode Compar | misaligned | smartpin-mode-constant-m | A gated frequency counter is built with P_COUNT_HIGHS, X=gat |
| p2-io-and-smart-pins-user-guide | part-5-appendices/appendix-e-tro | misaligned | debug-diagnostic-wrong-r | This DEBUG line reads and reports the pin's DIR (direction)  |
| p2-io-and-smart-pins-user-guide | part-5-appendices/appendix-e-tro | misaligned | single-pin-read-shift-al | Right-shifting PINREAD(pin) by 31 extracts the meaningful bi |
| p2-io-and-smart-pins-user-guide | part-5-appendices/appendix-e-tro | misaligned | debug-diagnostic-wrong-r | This DEBUG line reads and reports the pin's OUT (output) sta |
| p2-io-and-smart-pins-user-guide | appendix-f-mode-reference.md, Mo | misaligned | smartpin-register-mappin | In repository mode the value-to-store register is 'Y via WXP |
| p2-io-and-smart-pins-user-guide | part-5-appendices/appendix-f-mod | misaligned | sync-rx-x5-mode-mislabel | For P_SYNC_RX, X[5] Mode: 0=continuous, 1=start-stop |
| p2-io-and-smart-pins-user-guide | part-5-appendices/appendix-f-mod | misaligned | sync-rx-x5-mode-mislabel | WXPIN(pin, %1_00111) commented 'Start-stop, 8 bits' for P_SY |

## YAML-wrong findings → routed to P2KB-CORRECTION-FINDINGS.md

- **p2-io-and-smart-pins-user-guide chapter-04-smart-pin-configuration.md §4.13, line 542 (doc correct; YAML wrong)** — p2kbPasm2Rdpin.in_flag_reset_latency: 'RDPIN result,#pin / NOP  Clock 1 for IN flag reset / NOP  Clock 2 for IN flag reset / TESTP #pin WC': A single NOP elapses 2 clocks, which is exactly the 2-clock acknowledge delay — one NOP suffices. The doc statement is CORRECT and matches Tier 1.