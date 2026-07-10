# Fabrication-Audit Correctness Sweep — Change Catalog (change-first)

**Sprint:** Fabrication Audit & Correctness Sweep — §6 class-wide sweep (task #178)  
**Generated:** 2026-07-10 · **Spec:** fan-out v1.1.0  
**Scope:** confirmed `misaligned`/`fabricated` findings from the §5 fan-out (13 docs) + Assembly Part I pilot. Operator `=/==` class and ALL YAML edits are HELD for the separate plan-gate (not here). 59 `unverifiable` findings are NOT applied (flagged separately).

**Applied:** 342 changes across 56 files, in **275 distinct defect classes** + 17 extra same-class instances swept. **Genuine skips:** 2.

**How to read:** each change is described **once** with its true fact and source proof, then a table lists every document + location it was applied to (with before → after). Cross-check against `git diff` for the exact landed text. Every code change was compiled with `pnut_ts`.

**Source-proof / master-status principle:** no change was made without a Tier-1 citation (Parallax v35 Instructions CSV / P2 Silicon Doc v35 / Spin2 v55 / pnut_ts). The 'Correct (true fact)' + 'Source' lines below are that proof.

---

## C-01: `cycle-count-vs-instruction-count` — 10 sites · Assembly (Part I), DeSilva

- **The defect:** Almost twice as fast! (the 'after optimization' loop that merged the pointer increment into wrlong ptra++)
- **Correct (true fact):** The optimization removes exactly one 2-clock ADD from an ~18-20 clock loop (before ~18-20, after ~16-18). That is a ~10% speedup, not ~2x.
- **Source proof:** v35 CSV rows 154/223/169 (RDLONG/WRLONG/DJNZ) + ADD=2

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.11 medicine-cabin | A dedicated polling cog (testp / if_nz jmp / drvh) 'responds in ~4 clocks' → A dedicated cog responds in roughly 6-12 clocks (polling loop is 6 clocks; minim |
| DeSilva | Chapter 12 §The Hook, COMPLETE-OPUS-MASTER.m | Almost twice as fast! (the 'after optimization' loop that merged the pointer inc → Roughly one instruction (2 clocks) saved per iteration — about a 10% speedup, no |
| DeSilva | Chapter 12 §REP The Speed Loop, COMPLETE-OPU | That's 33% faster just by using REP! (2-add loop with djnz vs REP-wrapped 2 adds → About 50% faster per iteration once the taken DJNZ (4 clocks) is counted; 33% as |
| DeSilva | Chapter 12 §The FIFO Fast Path, COMPLETE-OPU | djnz count, #.loop costs 2 clocks (in the FIFO read loop) → djnz count, #.loop — 4 clocks when the loop branches back (2 only on the final f |
| DeSilva | Chapter 12 §medicine-cabinet, COMPLETE-OPUS- | Just these three changes (PTRA/PTRB, alignl, REP) often double performance → These are good habits but typically shave overhead instructions off a hub-bound  |
| DeSilva | Appendix A, "Deterministic Timing" subsectio | nearly all instructions execute in exactly 2 clock cycles ... Count the instruct → Most cog-register ALU/logic instructions take exactly 2 clocks, so multiply-by-2 |
| Assembly (Part I) | chapter-03-flags.md §3.3.1 line 207 | This three-instruction sequence (cmp + if_z mov + if_nz mov) takes exactly three → The sequence takes six clock cycles (three instructions × 2 clocks each) regardl |
| Assembly (Part I) | chapter-03-flags.md §3.3.2 line 223 | The test / if_nz rdlong / if_nz add sequence takes exactly three clock cycles wh → When not ready the sequence is 6 clocks (3×2); when ready it is 2 + (variable RD |
| Assembly (Part I) | chapter-03-flags.md §3.3.2 line 233 | The branch version takes 2 cycles when not ready (test + jump) or 4 cycles when  → Not-ready ≈ 6 clocks (test 2 + taken JMP ~4); ready ≈ 15-32 clocks (test 2 + not |
| Assembly (Part I) | chapter-03-flags.md §3.5.5 line 453 | No branches are needed, and timing is deterministic—two clock cycles regardless  → The test-plus-conditional-add pattern takes four clock cycles (2 + 2), determini |

## C-02: `pinfloat-disables-internal-pull` — 6 sites · IOSP

- **The defect:** Configuring `WRPIN(pin, P_HIGH_15K)` then `PINFLOAT(pin)` produces an active 15kΩ internal pull-up to VDD on an input pin.
- **Correct (true fact):** P_HIGH_15K only sets the drive-HIGH strength; that weak driver is active only when the pin's output is enabled (DIR=1, OUT=1). PINFLOAT clears DIR to 0, disabling all pin drive — so the internal 15kΩ pull-up is NOT active and the pin floats.
- **Source proof:** Silicon Doc p2-documentation.txt:7499 "Normally, an I/O pin's output enable is controlled by its DIR bit"; YAML p2kbSpin2Pinfloat: PINFLOAT sets DIR=0, "Pin will not drive any current in this state"

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-12-digital-input. | Configuring `WRPIN(pin, P_HIGH_15K)` then `PINFLOAT(pin)` produces an active 15k → To use the internal 15kΩ high-side driver as a pull-up, keep the pin driving: `W |
| IOSP | part-3-input-modes/chapter-12-digital-input. | `WRPIN(pin, P_LOW_15K)` then `PINFLOAT(pin)` produces an active 15kΩ internal pu → For a 15kΩ internal pull-down use `WRPIN(pin, P_LOW_15K)` then `PINLOW(pin)` (DR |
| IOSP | part-3-input-modes/chapter-12-digital-input. | `WRPIN(pin, P_SCHMITT_A \| P_HIGH_15K)` then `PINFLOAT(pin)` gives a Schmitt inp → Set the Schmitt mode with `WRPIN(pin, P_SCHMITT_A \| P_HIGH_15K)`, then enable t |
| IOSP | part-3-input-modes/chapter-12-digital-input. | Unused-pin 'Option 2: Pull-down' via `WRPIN(unused_pin, P_LOW_150K)` + `PINFLOAT → To hold an unused pin low use `WRPIN(unused_pin, P_LOW_150K)` then `PINLOW(unuse |
| IOSP | part-3-input-modes/chapter-12-digital-input. | Unused-pin 'Option 3: Pull-up' via `WRPIN(unused_pin, P_HIGH_150K)` + `PINFLOAT( → To hold an unused pin high use `WRPIN(unused_pin, P_HIGH_150K)` then `PINHIGH(un |
| IOSP | part-3-input-modes/chapter-12-digital-input. | button_init configures `WRPIN(BUTTON_PIN, P_HIGH_15K) ' Internal pull-up` then ` → Keep DIR high for the internal pull-up: `WRPIN(BUTTON_PIN, P_HIGH_15K)` then `PI |

## C-03: `gio-used-as-signal-input` — 5 sites · IOSP

- **The defect:** Configures 8 consecutive pins as ADC channels with P_ADC_GIO and then RDPINs each (line 395) as channel readings.
- **Correct (true fact):** P_ADC_GIO routes the pin group's INTERNAL GROUND reference to the ADC/IN. It does not sample the external pin, so RDPIN returns the ground-calibration reading (~0), not a per-channel signal.
- **Source proof:** spin2-v55-text.txt L1466: '%...1000000000000... \| P_ADC_GIO \| ADC GIO -> IN'; p2-documentation.txt M[9:7]=%000 source-select

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-16-adc.md §16.6 multi_adc_init, line | Configures 8 consecutive pins as ADC channels with P_ADC_GIO and then RDPINs eac → To read a signal on each pin use P_ADC_1X (or a gain mode); reserve P_ADC_GIO fo |
| IOSP | chapter-16-adc.md §16.7 Example 1 'Simple Po | An example titled 'Simple Potentiometer Reading' configures POT_PIN with P_ADC_G → WRPIN(POT_PIN, P_ADC_1X \| P_ADC) — unity-gain pin read is the correct source fo |
| IOSP | chapter-16-adc.md §16.7 Example 2 'Audio Sam | Configures AUDIO_PIN with P_ADC_GIO and captures a SINC2-filtered audio buffer o → For the AC/electret source described in the accompanying note use P_ADC_FLOAT (s |
| IOSP | chapter-16-adc.md §16.7 Example 2 note, line | Frames P_ADC_GIO as a 'ground-referenced' pin-input mode from which one would 's → This example should use P_ADC_FLOAT (or P_ADC_1X); P_ADC_GIO does not read the p |
| IOSP | chapter-16-adc.md §16.7 Example 5 PASM2 ADC, | PASM2 example configures ADC_PIN with P_ADC_GIO, then event-detects and threshol → Use ##P_ADC_1X \| P_ADC (or a gain mode) so the sampled/threshold-compared value |

## C-04: `hub-loop-cycle-understatement` — 4 sites · DeSilva

- **The defect:** Before optimization: 13 clocks (for the rdlong/add/wrlong/add/djnz loop)
- **Correct (true fact):** Sum of the instructions' own minimum clocks = 9+2+3+2+2 = 18 clocks; typical/average is ~20+ (hub-slot waits, taken branch). 13 is below the sum of minimums and unreachable.
- **Source proof:** v35 CSV row 154 RDLONG 9...16; row 223 WRLONG 3...10; row 169 DJNZ 2 or 4; ADD=2

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Chapter 12 §The Hook, COMPLETE-OPUS-MASTER.m | Before optimization: 13 clocks (for the rdlong/add/wrlong/add/djnz loop) → ~18 clocks minimum (9+2+3+2+2); realistically ~20+ per iteration with hub-slot w |
| DeSilva | Chapter 12 §The FIFO Fast Path, COMPLETE-OPU | Traditional hub reading (rdlong ptra++ / add / djnz loop): ~6 clocks average per → ~13 clocks minimum, ~16-18 average per long (RDLONG alone is 9-16). |
| DeSilva | Chapter 12 §Real-World Example Fast Memory C | copy_basic (rdlong/wrlong/add/add/djnz) runs ~13 clocks per long → ~18 clocks minimum, ~25 average per long for the rdlong/wrlong/add/add/djnz copy |
| DeSilva | Chapter 12 §Real-World Example Fast Memory C | copy_better (rdlong ptra++ / wrlong ptrb++ / djnz) runs ~8 clocks per long → ~14 clocks minimum (RDLONG 9 + WRLONG 3 + DJNZ 2), ~18+ average per long. |

## C-05: `packing-signedness-misattribution` — 4 sites · Debug Window

- **The defect:** LONGS_16BIT is sign-extended and the WORDS_*/BYTES_* modes are zero-extended (signedness is a property of the packing keyword).
- **Correct (true fact):** packed_data_mode {ALT} {SIGNED}; 'The SIGNED keyword will cause all unpacked data values to be sign-extended.' LONGS_16BIT default Final Values 0..65,535 (unsigned); SIGNED gives -32,768..32,767. Every mode is unsigned/zero-extended by default and sign-extended only when SIGNED is appended.
- **Source proof:** Spin2 v55 text.txt lines 1401-1417 (Packed-Data Modes table + rules)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch10-spectro.md §Feeding samples, lines 107- | LONGS_16BIT is sign-extended and the WORDS_*/BYTES_* modes are zero-extended (si → All packing modes deliver unsigned (zero-extended) values by default; appending  |
| Debug Window | ch10-spectro.md §Feeding samples, lines 98-9 | The packing keyword itself selects whether the samples are sign-extended. → A packing keyword selects how many samples each long carries; a separate optiona |
| Debug Window | ch10-spectro.md §Feeding samples, lines 102- | LONGS_8BIT (without SIGNED) delivers four signed bytes; the byte $C0 becomes a s → To feed signed bytes the mode must be `LONGS_8BIT SIGNED`; as written, the four  |
| Debug Window | ch10-spectro.md §Feeding samples, line 110 | LONGS_8BIT carries four 8-bit signed samples per long. → LONGS_8BIT carries four 8-bit samples per long (a 4× gain); they are signed only |

## C-06: `usb-pair-upper-pin-wrpin-omitted` — 4 sites · IOSP

- **The defect:** The Basic Configuration example issues WRPIN only on USB_DM (lower pin), then PINHIGH on both USB_DM and USB_DP, never running WRPIN on the upper (DP) pin.
- **Correct (true fact):** BOTH pins of the USB pair must EACH be configured via WRPIN with identical D data %1_11011_0 before their DIR bits are raised; only WXPIN/WYPIN/RDPIN are lower-pin-only.
- **Source proof:** Silicon Doc p2-documentation.txt:8902-8904 ('clear the DIR bits of the intended two pins and configure them each via WRPIN') + :8884-8885 ('They can be configured via WRPIN with identical D data of %1_11011_0')

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-4-special-modes/chapter-19-usb.md §19.2 | The Basic Configuration example issues WRPIN only on USB_DM (lower pin), then PI → Also issue WRPIN(USB_DP, P_USB_PAIR \| P_OE) (identical D data) on the upper pin |
| IOSP | part-4-special-modes/chapter-19-usb.md §19.7 | The §19.7 Spin2 configure_usb() example PINFLOATs both pins, WRPINs only USB_DM, → Add WRPIN(USB_DP, P_USB_PAIR \| P_OE) before PINHIGH(USB_DP); the upper pin need |
| IOSP | part-4-special-modes/chapter-19-usb.md §19.7 | The §19.7 PASM2 example does dirl on both pins, wrpin usb_mode only on #USB_DM,  → Add 'wrpin usb_mode, #USB_DP' (identical D data) before 'dirh #USB_DP'. |
| IOSP | part-4-special-modes/chapter-19-usb.md §19.1 | The Quick Reference 'Configuration Pattern' WRPINs only even_pin, then PINHIGHs  → Add WRPIN(even_pin+1, P_USB_PAIR \| P_OE) before PINHIGH(even_pin+1) in the quic |

## C-07: `color-format-rgb24-vs-named` — 3 sites · Debug Window

- **The defect:** COLOR takes lit-key colors specified as `$RRGGBB` 24-bit hex values.
- **Correct (true fact):** For the MIDI window, COLOR accepts NAMED colors plus optional 0..15 brightness — NOT rgb24 hex. The SCOPE/PLOT/etc. footnotes explicitly begin 'Color is rgb24 value, else...' (lines 1142/1172/1197/1225); the MIDI (1395) and LOGIC (1320) footnotes deliberately omit 'rgb24 value, else', so rgb24 is not a documented MIDI COLOR format.
- **Source proof:** Spin2 v55 line 1395 (MIDI COLOR footnote): 'Color is BLACK / WHITE or ORANGE / BLUE / GREEN / CYAN / RED / MAGENTA / YELLOW / GRAY followed by an optional 0..15 for brightness'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch11-midi.md §Creating a MIDI window, line 4 | COLOR takes lit-key colors specified as `$RRGGBB` 24-bit hex values. → COLOR takes two named colors (e.g. GREEN, ORANGE) each with optional 0..15 brigh |
| Debug Window | ch11-midi.md §Creating a MIDI window, line 7 | A MIDI window can be given lit colors via COLOR $00FF00 $FF7F00 (rgb24 green/ora → Use named colors, e.g. `COLOR GREEN ORANGE` (optionally with a 0..15 brightness  |
| Debug Window | ch11-midi.md §A complete software-only examp | The velocity example creates a MIDI window with COLOR $00FF00 $FF7F00 (rgb24). → Use named colors, e.g. `COLOR GREEN ORANGE`. |

## C-08: `debug-window-range-mismatch` — 3 sites · Debug Window

- **The defect:** LOGIC LINESIZE range is 1–32.
- **Correct (true fact):** LOGIC LINESIZE is 1_to_7 (default 1), NOT 1–32. 1–32 is the SCOPE/FFT LINESIZE range, not LOGIC's.
- **Source proof:** Spin2 v55 text line 1127: '\| LINESIZE 1_to_7 \| Set the line size. \| 1'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | Appendix A, LOGIC configuration directives t | LOGIC LINESIZE range is 1–32. → LOGIC `LINESIZE` per the v55 reference is 1–7 (default 1); confirm against PNut  |
| Debug Window | Appendix A, LOGIC configuration directives t | LOGIC SAMPLES range is 4–2047. → LOGIC `SAMPLES` is 4–2048 per the v55 reference (default 32). |
| Debug Window | Appendix A, LOGIC configuration directives t | LOGIC SPACING range is 1–32. → LOGIC `SPACING` is 2–32 per the v55 reference (default 8). |

## C-09: `hub-overlap-fabrication` — 3 sites · Assembly (Part I)

- **The defect:** a program can issue a hub access and immediately begin computing with data already available, allowing the hub access to proceed in parallel
- **Correct (true fact):** 'If an instruction stalls for additional clock cycles, all following instructions in the pipeline are also stalled.' A scalar RDLONG blocks the cog for its full 9...16 clocks; subsequent instructions do NOT execute during the hub access. There is no non-blocking scalar hub read.
- **Source proof:** Silicon Doc v35 lines 629-630 (pipeline stall); CSV RDLONG cog clocks 9...16

TODO: can we source a narrative description of this our p2 eggbeater paradigm? Don't we expect a delay in the first access but not on subsequent accesses?  I'm not sure, i'm asking to make sure we carefully understand this.

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.6.2 Pipelined Hub Ac | a program can issue a hub access and immediately begin computing with data alrea → A plain RDLONG blocks the cog until the read completes; the following instructio |
| Assembly (Part I) | chapter-04-timing.md §4.6.2 Pipelined Hub Ac | The SETQ-based burst transfer provides one form of pipelining—while later longs  → The SETQ+RDLONG burst blocks the cog for the whole transfer (~26-33 clocks per § |
| Assembly (Part I) | chapter-04-timing.md §4.6.2 Pipelined Hub Ac | This pattern keeps hub access and computation overlapped—the RDLONG for iteratio → Reordering the loop so the next read is issued before processing the current dat |

## C-10: `invented-default-value` — 3 sites · Debug Window

- **The defect:** TEXTSIZE default is 10 points
- **Correct (true fact):** TEXTSIZE default is the editor text size (configurable), not a fixed 10. Range 6-200 is correct.
- **Source proof:** Spin2 v55 line 1128: 'TEXTSIZE 6_to_200 \| ... \| editor text size'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md config-keyword table, line 63  | TEXTSIZE default is 10 points → TEXTSIZE: default = editor text size, range 6–200. |
| Debug Window | ch06-logic.md config-keyword table, line 56  | TITLE default text is 'Logic' → TITLE: default <none> (the window caption is unset unless TITLE is given; typica |
| Debug Window | ch06-logic.md config-keyword table, line 57  | POS default is 'cascaded' → POS: default 0, 0. |

## C-11: `nco-frequency-resolution-inverted` — 3 sites · IOSP

- **The defect:** X[15:0] = 1 provides best frequency resolution.
- **Correct (true fact):** Frequency step per unit of Y = sysclk/(X*2^32); a LARGER X gives a SMALLER (finer) step, i.e. finer frequency resolution. X=1 gives the COARSEST resolution (but widest range / max update rate).
- **Source proof:** Silicon Doc part4-smart-pins.txt %00110 (Y added into Z at each base period; X[15:0]=base period clocks) + chapter's own formula line 55: frequency=(Y*sysclk)/(X[15:0]*2^32)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-08-nco-frequency | X[15:0] = 1 provides best frequency resolution. → X[15:0]=1 gives the maximum output-frequency range and update rate; frequency re |
| IOSP | part-2-output-modes/chapter-08-nco-frequency | X[15:0]=1 gives Maximum resolution (200,000,000 updates/sec). → Label should read 'Maximum range / update rate' (or 'least jitter'), not 'Maximu |
| IOSP | part-2-output-modes/chapter-08-nco-frequency | Base period X[15:0] = 1 for maximum resolution. → '1 for maximum frequency range / update rate' — X=1 is not maximum frequency res |

## C-12: `operator-precedence-order-inversion` — 3 sites · Assembly (Part I)

- **The defect:** Under 'listed from highest to lowest precedence', the arithmetic table lists + and - before *, /, +/, //, +//
- **Correct (true fact):** In Spin2, *, /, +/, //, +// have precedence 7 (bind TIGHTER); + and - have precedence 8 (bind looser). Multiplication/division bind tighter than addition/subtraction.
- **Source proof:** Spin2 v55 operator table: * / +/ // +// = Term Priority 7; + - = Term Priority 8 (spin2-v55-text.txt lines ~453-467)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.9.2 Arit | Under 'listed from highest to lowest precedence', the arithmetic table lists + a → Per the doc's own stated rule ('listed from highest to lowest precedence within  |
| Assembly (Part I) | chapter-02-instruction-format.md §2.9.2 Bitw | Under 'highest to lowest precedence', the bitwise table lists \| (OR) before ^ ( → Per the doc's stated highest-to-lowest ordering, ^ (Bitwise XOR) must be listed  |
| Assembly (Part I) | chapter-02-instruction-format.md §2.9.2 Bool | Under 'highest to lowest precedence', the boolean table lists \|\| before ^^, an → Per highest-to-lowest ordering, ^^ must precede \|\| (doc has \|\| before ^^). A |

## C-13: `pasm-immediate-address-vs-value` — 3 sites · IOSP

- **The defect:** Example 3 configures and polls BUTTON_PIN (pin 20); `mov pin, #BUTTON_PIN` is presented as loading the pin number into `pin`.
- **Correct (true fact):** BUTTON_PIN is defined as `long 20` at cog address 9; `mov pin, #BUTTON_PIN` loads the immediate 9 (the address), so the loop polls pin 9, not pin 20. To load the value 20 the code must read the long's contents: `mov pin, BUTTON_PIN` (no `#`).
- **Source proof:** pnut-ts 1.55 listing of the example: symbol BUTTON_PIN resolves to cog long address 0x09 (VALUE 00900024). PASM2 `#label` supplies the label's address, not its stored value.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-12-digital-input. | Example 3 configures and polls BUTTON_PIN (pin 20); `mov pin, #BUTTON_PIN` is pr → Use `mov pin, BUTTON_PIN` (no `#`) to load the value 20, or define BUTTON_PIN in |
| IOSP | chapter-13-timing-measurement.md §13.7 Examp | Example 3 ("PASM2 High-Speed Frequency Counter") configures/reads the smart pin  → Either define the pin as a CON symbol (`CON FREQ_PIN = 20`) and use `#FREQ_PIN`, |
| IOSP | chapter-13-timing-measurement.md §13.7 Examp | `wrlong period, #period_hub` stores the period to hub so the main cog can read i → Use a real hub variable (a VAR/DAT long in hub) and pass its hub address (e.g. v |

## C-14: `smartpin-mode-constant-mismatch` — 3 sites · IOSP

- **The defect:** P_COUNT_HIGHS measures 'Gated edges' and is used as a 'Freq counter'.
- **Correct (true fact):** P_COUNT_HIGHS (%01111) accumulates clocks while A is high (a high-time/duty measurement); it does NOT count gated edges. The gated-edge counter (inc on A-rise while B-high) is P_REG_UP (%01100).
- **Source proof:** Spin2 v55 line 1545 (P_COUNT_HIGHS=%01111 'Inc on A-high, optionally dec on B-high'); silicon part4-smart-pins line 625 (%01111 = Count A-input highs); P_REG_UP=%01100 'Inc on A-rise when B-high' (Spin2 line 1542)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-d §Input Mode Comparison, line 35 | P_COUNT_HIGHS measures 'Gated edges' and is used as a 'Freq counter'. → The gated-edge frequency-counter row should name P_REG_UP with measurement 'gate |
| IOSP | appendix-d §Counting Mode Comparison, line 9 | A gated frequency counter is built with P_COUNT_HIGHS, X=gate_period. → Gated frequency counter → P_REG_UP (count A-rise while B-high), or P_COUNT_RISES |
| IOSP | appendix-d §Counting Mode Comparison, line 9 | A step/direction motor counter uses P_COUNT_RISES with X=0. → Step/direction motor → P_REG_UP_DOWN (A=step, B=direction level). |

## C-15: `abs-c-flag-edge-case-fabrication` — 2 sites · Assembly (Part I)

- **The defect:** The ABS instruction handles this by leaving the value unchanged and setting C to indicate the exceptional case.
- **Correct (true fact):** ABS with WC sets C = the ORIGINAL sign bit (S[31]/D[31]); C=1 for EVERY negative source, not just the unrepresentable $8000_0000. C is not an edge-case indicator.
- **Source proof:** v35 CSV row 62 (ABS): 'Get absolute value of D into D. D = ABS(D). C = D[31].' — two-operand encoding c=S[31]

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.5.4 line 431 | The ABS instruction handles this by leaving the value unchanged and setting C to → ABS with WC sets C to the original sign bit — C=1 whenever the source was negati |
| Assembly (Part I) | chapter-03-flags.md §3.5.4 line 433 | For all other negative values, ABS correctly computes the absolute value and cle → For every negative value ABS computes the absolute value and SETS C (C = origina |

## C-16: `adc-pin-power-group-size-four-vs-eight` — 2 sites · P2AN001

- **The defect:** the P2 powers its I/O pins in isolated groups of four, and a pin's ADC measures the VIO/GIO of its own group
- **Correct (true fact):** The P2's 64 I/O pins are powered in 8 isolated groups of EIGHT (P0-7, P8-15, ... P56-63); each group has its own VIO/GIO reference pair. The number is eight, not four.
- **Source proof:** Silicon Doc p2-documentation.txt L511-517 (VIO_{x}_{y}/GIO_{x}_{y} = 'Power/Ground for smart pins {x} through {y}'); hardware-verification VERIFICATION-OPPORTUNITIES.md:57; edge-module-breakout-compatibility-matrix.md:70 ('300mA per 8-pin group') / L75 ('V00: Powers P0-P7')

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN001 | P2AN001.md §How It Works (in brief), line 47 | the P2 powers its I/O pins in isolated groups of four, and a pin's ADC measures  → the P2 powers its I/O pins in isolated groups of eight (P0-7, P8-15, ... P56-63) |
| P2AN001 | P2AN001.md §Recipe 2, line 247 | Those four are one complete 4-pin power group (32–35), so the three measurement  → Those four pins all sit inside power group P32-39 (an 8-pin group), so the three |

## C-17: `alt-modifier-semantics-wrong` — 2 sites · Debug Window

- **The defect:** ALT — the host swaps adjacent same-width fields throughout the element: neighbouring bits (0↔1, 2↔3, …) ... a butterfly swap of neighbours across the whole long, not a within-byte or end-to-end reversal.
- **Correct (true fact):** The ALT keyword will cause bits, double-bits, or nibbles, within each byte sent, to be reordered end-to-end on the host side, within each byte.
- **Source proof:** Spin2 v55 text line 1403 (Packed-Data Modes section)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch13-packed-data.md §The ALT and SIGNED modi | ALT — the host swaps adjacent same-width fields throughout the element: neighbou → ALT reorders the sub-units (bits, double-bits, or nibbles) end-to-end WITHIN EAC |
| Debug Window | ch13-packed-data.md §Considerations, lines 2 | Use ALT only to swap adjacent same-width fields throughout the element (bits 0↔1 → ALT reverses the order of the sub-units (bits / double-bits / nibbles) end-to-en |

## C-18: `bit-dac-nibbles-unset-no-output` — 2 sites · IOSP

- **The defect:** NCO frequency mode combined with P_DAC_990R_3V generates a square wave that, with external RC filtering, approximates a sine wave.
- **Correct (true fact):** In DAC_MODE a non-DAC smart pin mode (NCO %00110) does NOT feed the 8-bit DAC; its 1-bit SMART output drives BIT_DAC, selecting between the two 4-bit nibbles M[7:4] and M[3:0]. P_DAC_990R_3V sets M[7:0]=0, so both BIT_DAC levels are code 0 = 0V. The pin sits at 0V regardless of NCO toggling — no square wave is produced.
- **Source proof:** Silicon Doc part4-smart-pins.txt lines 70,103-104: non-DAC smart modes (%00100..%11111) drive BIT_DAC in DAC_MODE; BIT_DAC outputs {2{M[7:4]}}/{2{M[3:0]}}

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-10-dac-output.md | NCO frequency mode combined with P_DAC_990R_3V generates a square wave that, wit → To emit a square wave via NCO+BIT_DAC you must set the two DAC nibbles (e.g. M[7 |
| IOSP | part-2-output-modes/chapter-10-dac-output.md | PWM triangle mode combined with P_DAC_600R_2V produces smooth analog PWM output  → As with the NCO example, the two BIT_DAC nibble levels (M[7:4], M[3:0]) must be  |

## C-19: `color-name-green-vs-lime` — 2 sites · Debug Window

- **The defect:** Default TERM color pairs 2 and 3 use foreground/background color 'Lime'.
- **Correct (true fact):** The default color combos #2 and #3 use GREEN, not 'Lime'. The P2 debug palette keywords are BLACK/WHITE/ORANGE/BLUE/GREEN/CYAN/RED/MAGENTA/YELLOW/GRAY — there is no 'Lime'.
- **Source proof:** Spin2 v55 TERM Instantiation, COLOR default: '2 = GREEN/BLACK 3 = BLACK/GREEN' (spin2-v55-text.txt line ~1306)

TODO: need to audit against detail document from pnut-ts (in pnut-ts-facts/ folder maybe)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch03-term.md §Color / default color table, l | Default TERM color pairs 2 and 3 use foreground/background color 'Lime'. → Pair 2 = Green/Black, Pair 3 = Black/Green (the default keyword is GREEN, not Li |
| Debug Window | ch03-term.md §A positioned dashboard, line 2 | Color pair 2 (code 6) is 'lime'. → Pair 2 is green (Green/Black) under the default palette. |

## C-20: `dac-mode-dithering-overgeneralization` — 2 sites · IOSP

- **The defect:** the repository modes (%00001-%00011) ... serve dual purposes: ... and high-resolution DAC output with dithering
- **Correct (true fact):** %00001 in DAC_MODE = 'DAC noise' (overrides M[7:0] to feed the 8-bit DAC pseudo-random data); only %00010/%00011 are 16-bit dither modes.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 111-113, 235-238

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-4-special-modes/chapter-18-repository.m | the repository modes (%00001-%00011) ... serve dual purposes: ... and high-resol → ...serve dual purposes: long repository, and DAC output — pseudo-random noise (% |
| IOSP | part-4-special-modes/chapter-18-repository.m | DAC_MODE (P[12:10]=%101) => DAC with dithering → DAC_MODE => DAC output: noise (%00001) or 16-bit dithered (%00010/%00011). |

## C-21: `debug-diagnostic-wrong-register` — 2 sites · IOSP

- **The defect:** This DEBUG line reads and reports the pin's DIR (direction) state.
- **Correct (true fact):** PINREAD returns the IN (input) pin state, not the DIR/direction bit. DIR is held in the DIRA register.
- **Source proof:** Spin2 v55 line 536: 'PINREAD (PinField) : PinStates \| Read PinField pin(s)'; line 360: INA/OUTA/DIRA table (INA=Input states, DIRA=Output enables)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-e-troubleshooting | This DEBUG line reads and reports the pin's DIR (direction) state. → To read DIR use `(DIRA >> pin) & 1`; PINREAD(pin) returns the IN state, which is |
| IOSP | part-5-appendices/appendix-e-troubleshooting | This DEBUG line reads and reports the pin's OUT (output) state. → To read the OUT state use `(OUTA >> pin) & 1` (and only for pins 0-31; use OUTB  |

## C-22: `default-value-mismatch` — 2 sites · Debug Window

- **The defect:** The default TITLE (title-bar text) of a MIDI window is `MIDI`.
- **Correct (true fact):** The documented default for TITLE is <none>, not the literal string 'MIDI'. In PNut the caption falls back to the window's given name (e.g. 'Piano'), not the window type.
- **Source proof:** Spin2 v55 line 1383: 'TITLE 'string' \| Set the window caption to 'string'. \| <none>'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch11-midi.md §Creating a MIDI window, line 4 | The default TITLE (title-bar text) of a MIDI window is `MIDI`. → TITLE default is <none> (the window shows its given name, e.g. 'Piano', when no  |
| Debug Window | ch11-midi.md §Creating a MIDI window, line 4 | The default POS (screen position) of a MIDI window is `auto`. → POS default is 0, 0 (top-left of the screen) per the Spin2 v55 MIDI table. |

## C-23: `enob-vs-nominal-bits-reframing` — 2 sites · IOSP

- **The defect:** SINC3 ... doubling the effective bits for fast-changing signals
- **Correct (true fact):** 'SINC3 doubles the ENOB (effective number of bits) over simple bit-summing for fast signals, but it is only slightly better at DC measurements than SINC2.' Doubling is vs simple bit-summing, NOT vs SINC2.
- **Source proof:** Silicon Doc v35, part4-smart-pins.txt line 886

TODO We have to be VERY careful here, "ENOB" is a specific term and likely doens't apply... we have to choose our terminology extremely carefully  - we just make a sweeping ENOB correctness page prior to this.  We can't re-introduce".

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §16.3 SINC3 Filtering Mode (%10), line 192 | SINC3 ... doubling the effective bits for fast-changing signals → SINC3 gives better dynamic response than SINC2; it roughly doubles the nominal b |
| IOSP | §16.3 Resolution and Sample Rate, SINC3 foot | the higher SINC3 figures assume an idealized doubling over SINC2 → The SINC3 figures assume an idealized doubling over simple bit-summing that the  |

## C-24: `false-chapter-backreference` — 2 sites · Getting Started

- **The defect:** the P2 gives you **locks** (the 16 hardware locks from Chapter 1) to guard the exchange
- **Correct (true fact):** The P2 does have 16 locks (16 semaphore bits with atomic read-modify-write), so the number is correct; but Chapter 1 of THIS guide never introduces locks at all -- its closing cast list (line 302-305) omits locks.
- **Source proof:** Silicon Doc p2-documentation.txt:435 (16 semaphore bits); this-doc Ch1 lines 21-309 grep 'lock' -> zero matches (only 'clock'/'block')

| Document | Location | before → after |
|----------|----------|----------------|
| Getting Started | getting-started-body.md Ch3 §"Sharing data b | the P2 gives you **locks** (the 16 hardware locks from Chapter 1) to guard the e → The fact '16 hardware locks' is correct, but the phrase 'from Chapter 1' is wron |
| Getting Started | getting-started-body.md Ch3 §"Spin2 or PASM2 | it runs at the deterministic two-clocks-per-instruction speed from Chapter 1 → 'from Chapter 1' correctly covers the determinism claim but not the two-clocks-p |

## C-25: `frame-field-16bit-overflow` — 2 sites · IOSP

- **The defect:** Choose: Base period = 1, Frame period = 100,000  → PWM period = 2 × 100,000 × 1 = 200,000 clocks ✓
- **Correct (true fact):** The frame period lives in bits [31:16] of X — a 16-bit field whose maximum value is 65535 (65536 at most). A frame period of 100,000 cannot be represented in that field.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt:429 ("X[31:16] establishes a PWM frame period") — X[31:16] is a 16-bit field, max 65535

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-09-pwm-output.md | Choose: Base period = 1, Frame period = 100,000  → PWM period = 2 × 100,000 × 1  → Frame period 100,000 exceeds the 16-bit X[31:16] field; split it across base and |
| IOSP | part-2-output-modes/chapter-09-pwm-output.md | frame := _clkfreq / (2 * freq_hz) ... WXPIN(PWM_PIN, 1 \| (frame << 16)) → The triangle_pwm routine must guard against frame > 65535: when _clkfreq/(2*freq |

## C-26: `gio-reference-used-as-signal-input` — 2 sites · IOSP

- **The defect:** read_adc configures P_ADC_GIO and returns RDPIN as the 'latest sample'
- **Correct (true fact):** P_ADC_GIO selects the chip's internal GROUND reference as the ADC input; §16.2 states it is 'a calibration source, not a signal input.' A read via P_ADC_GIO returns the ground reference, not a pin signal.
- **Source proof:** This doc §16.2 line 39/70 + Spin2 v55 line 1466 (P_ADC_GIO = ADC GIO -> IN)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §16.3 SINC2 Sampling Mode config example, li | read_adc configures P_ADC_GIO and returns RDPIN as the 'latest sample' → Use P_ADC_1X (pin, unity gain) as the input for a generic 'read the pin sample'  |
| IOSP | §16.5 scope_init config example, line 341 | scope_init configures the scope pin with P_ADC_GIO input select → Configure the scope pin with a pin input-select (e.g. P_ADC_1X \| P_ADC_SCOPE) s |

## C-27: `hub-access-2-base-model` — 2 sites · Assembly (Part I)

- **The defect:** The base instruction time is 2 cycles, but the wait for hub access adds 0 to 7 additional cycles ... (implying hub access totals 2-9 cycles).
- **Correct (true fact):** A standalone hub read (RDLONG) costs 9...16 clocks in cog mode — a 9-clock floor, not 2. The 0-7 figure is only the slot-wait component; total is never as low as 2.
- **Source proof:** v35 CSV row 154 (RDLONG): cog clocks '9...16'; hub '9...26'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.2.2 (prose under cyc | The base instruction time is 2 cycles, but the wait for hub access adds 0 to 7 a → Hub data-access instructions have a 9-clock floor (RDLONG 9...16 cog / 9...26 hu |
| Assembly (Part I) | chapter-04-timing.md §4.2.2 cycle-count tabl | Hub access \| 2-16+ (typical cycles) → Hub access \| 9-16 (cog) / 9-26 (hub-exec). |

## C-28: `hub-write-timing-understated` — 2 sites · Assembly (Part I)

- **The defect:** **Variable:** Hub operations (9-16 clocks in cog/LUT mode, 9-26 clocks in HUB mode)
- **Correct (true fact):** Hub READS take 9...16 (cog/LUT) / 9...26 (hub-exec) clocks, but hub WRITES take only 3...10 (cog/LUT) / 3...20 (hub-exec) clocks. The 9-16/9-26 figures are read-only.
- **Source proof:** v35 CSV rows 221-223 (WRBYTE/WRWORD/WRLONG) clock columns = 3...10 (cog/LUT, 8 cogs), 3...20 (hub, 8 cogs); vs rows 152-154 (RDBYTE/RDWORD/RDLONG) = 9...16 / 9...26

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-06-address-modes.md §6.8.1 Performan | **Variable:** Hub operations (9-16 clocks in cog/LUT mode, 9-26 clocks in HUB mo → Hub reads take 9-16 clocks (cog/LUT) or 9-26 (hub-exec); hub writes are faster a |
| Assembly (Part I) | chapter-06-address-modes.md §6.8.1 Timing No | Hub operations require ~9 base clocks plus 0-7 clocks waiting for the hub window → Hub reads require ~9 base clocks plus 0-7 window-wait clocks; hub writes require |

## C-29: `invert-a-vs-invert-b` — 2 sites · IOSP

- **The defect:** To select negative (falling) clock edge for P_SYNC_TX, add P_INVERT_A
- **Correct (true fact):** The sync-TX clock is registered on the B input (A-data, B-clock). Negative-edge clocking is obtained by inverting the B input = P_INVERT_B (B[3]), not the A input.
- **Source proof:** Silicon Doc p2-documentation.txt line ~9042 (%11100): 'For negative-edge clocking, the B input may be inverted by setting B[3] in WRPIN's D value'; Spin2 v55 lines 1423/1435: P_INVERT_A=Invert A input, P_INVERT_B=Invert B input

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | To select negative (falling) clock edge for P_SYNC_TX, add P_INVERT_A → Negative (falling) edge: Add P_INVERT_B (inverts the B/clock input) |
| IOSP | part-2-output-modes/chapter-11-serial-transm | For CPHA=1, use P_INVERT_A on the data pin → For CPHA=1, invert the clock edge seen by the data pin with P_INVERT_B (or inver |

## C-30: `luma-hsv-x-variant-mischaracterized` — 2 sites · Debug Window

- **The defect:** The W variants run from white toward the color; the X variants expand the value range.
- **Correct (true fact):** The X variant is a three-stop ramp black -> color -> white (brightest values peak in white). It does not 'expand' the 8-bit input value range.
- **Source proof:** Spin2 v55 color-mode table: 'LUMA8X \| 8 \| From black to color to white \| ...luminance indicates level, peaking in white'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch04-bitmap.md §Color modes / Luminance mode | The W variants run from white toward the color; the X variants expand the value  → The X variants ramp black -> color -> white (the top of the range peaks in white |
| Debug Window | ch04-bitmap.md §Color modes / HSV modes, lin | As with the luminance modes, W runs from white and X expands the range. → The X variants ramp black -> color -> white, peaking in white. |

## C-31: `maximum-toggle-rate-not-maximum` — 2 sites · IOSP

- **The defect:** Section titled 'Maximum Toggle Rate' presents drvnot+jmp (6 clocks/toggle) as the maximum: ~33 MHz edge rate / ~16.5 MHz square wave.
- **Correct (true fact):** The maximum toggle rate is 2 clocks per toggle using REP + DRVNOT (no branch overhead) = 100M toggles/s = 50 MHz square wave at 200 MHz. The drvnot+jmp loop pays the 4-clock branch on every edge (6 clocks/toggle), which is 3x slower than the true maximum.
- **Source proof:** Silicon Doc p2-documentation.txt lines 1710-1717: 'REP #1,##1000 / DRVNOT #0 ... output and toggle pin 0 (2 clocks per toggle)'; CSV rows 380 (DRVNOT=2 clk), 317 (JMP=4 clk)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-06-digital-output.md §6.4 'Maximum T | Section titled 'Maximum Toggle Rate' presents drvnot+jmp (6 clocks/toggle) as th → The drvnot+jmp tight loop toggles every 6 clocks (16.5 MHz square wave); this is |
| IOSP | chapter-06-digital-output.md §6.3 'Fast Togg | The drvh/drvl/jmp loop (8 clocks, 2 edges, 25 MHz signal) is labeled 'Maximum so → This loop produces a 25 MHz asymmetric signal (~4 clocks/toggle average); it is  |

## C-32: `nco-jitter-direction-inverted` — 2 sites · IOSP

- **The defect:** Using X[15:0] > 1 reduces update rate but can smooth jitter.
- **Correct (true fact):** Output edges are quantized to base-period boundaries; a LARGER base period (X>1) coarsens edge placement, so timing jitter INCREASES (up to one base period), it does not smooth.
- **Source proof:** Silicon Doc part4-smart-pins.txt %00110 (X[15:0]=base period in clock cycles; output reflects Z[31], toggles only at base-period boundaries)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-08-nco-frequency | Using X[15:0] > 1 reduces update rate but can smooth jitter. → Using X>1 reduces the update rate and INCREASES output edge jitter (coarser time |
| IOSP | part-2-output-modes/chapter-08-nco-frequency | X[15:0]=10 yields Reduced jitter. → X=10 gives coarser (worse) edge jitter; the benefit of X>1 is finer frequency re |

## C-33: `pick-one-orthogonal-fields` — 2 sites · IOSP

- **The defect:** A single 'pick one' table combines P_TRUE_A/P_INVERT_A (polarity) with P_LOCAL_A..P_MINUS1_A (pin selection), Bits [31:28].
- **Correct (true fact):** Invert (bit 31) is an independent field from the 3-bit A-input selector (bits 30:28); P_INVERT_A can be OR'd with any selection (e.g. P_INVERT_A \| P_PLUS1_A = %1001).
- **Source proof:** Spin2 v55 text lines 1421-1432: two SEPARATE '(pick one)' groups — 'A Input Polarity' (P_INVERT_A = bit31) and 'A Input Selection' (P_LOCAL_A..P_MINUS1_A = bits 30:28)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-b-p-constants.md §A Input Selection | A single 'pick one' table combines P_TRUE_A/P_INVERT_A (polarity) with P_LOCAL_A → Split into two independent choices: A-input polarity (P_TRUE_A / P_INVERT_A, bit |
| IOSP | appendix-b-p-constants.md §B Input Selection | A single 'pick one' table combines P_TRUE_B/P_INVERT_B (polarity) with P_LOCAL_B → Split into two independent choices: B-input polarity (P_TRUE_B / P_INVERT_B, bit |

## C-34: `smartpin-mode-invalid-config` — 2 sites · IOSP

- **The defect:** P_HIGH_TICKS is configured with X=period and Y=1 for differential timing.
- **Correct (true fact):** P_HIGH_TICKS (%10001) times high states continuously and takes no X (measurement-period) or Y parameter; the silicon description defines no X/Y inputs for this mode. A 'Y=1' setting is meaningless here.
- **Source proof:** silicon part4-smart-pins lines 669-678 (%10001 'Time A-input high states'); Spin2 v55 line 1547 (P_HIGH_TICKS 'For A-high states, count ticks')

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-d §Counting Mode Comparison, line 9 | P_HIGH_TICKS is configured with X=period and Y=1 for differential timing. → P_HIGH_TICKS needs no X/Y; drop the 'X=period, Y=1' configuration (that Y[0] up/ |
| IOSP | appendix-d §Counting Mode Comparison, line 9 | P_HIGH_TICKS is configured with X=period for PWM duty integration. → For a period-bounded duty measurement use P_PERIODS_HIGHS or P_COUNTER_HIGHS (wh |

## C-35: `sync-rx-x5-mode-mislabel` — 2 sites · IOSP

- **The defect:** For P_SYNC_RX, X[5] Mode: 0=continuous, 1=start-stop
- **Correct (true fact):** X[5] selects the A-input sample position relative to the B-input edge: X[5]=0 = sample just before the B edge (no sender hold time needed); X[5]=1 = sample coincident with the B edge. It is NOT a continuous/start-stop selector.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 9070-9076 (%11101 sync serial receive)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-f-mode-reference. | For P_SYNC_RX, X[5] Mode: 0=continuous, 1=start-stop → X[5] \| Sample position: 0 = sample just before B-input edge, 1 = sample coincid |
| IOSP | part-5-appendices/appendix-f-mode-reference. | WXPIN(pin, %1_00111) commented 'Start-stop, 8 bits' for P_SYNC_RX → ' Sample coincident with clock edge, 8 bits |

## C-36: `term-default-pair3-color` — 2 sites · Debug Window

- **The defect:** Selecting color pair 3 (code 7) in this example gives red 'HIGH' text.
- **Correct (true fact):** With default colors, pair 3 is BLACK-on-GREEN (black text on green background), not red. This example's creation line 'debug(`TERM Panel SIZE 40 8)' sets NO custom COLOR, so defaults apply.
- **Source proof:** Spin2 v55 TERM COLOR default: '3 = BLACK/GREEN' (spin2-v55-text.txt ~line 1306)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch03-term.md §A positioned dashboard, line 2 | Selecting color pair 3 (code 7) in this example gives red 'HIGH' text. → Under the default palette, code 7 (pair 3) renders black-on-green — the comment  |
| Debug Window | ch03-term.md §Try it, line 315 | Pair 3 is red; selecting it turns the value red. → Pair 3 is not red by default; to turn a value red the reader must first set a cu |

## C-37: `wrong-invert-constant-a-vs-in` — 2 sites · IOSP

- **The defect:** For RS-232 with external level shifter, invert the received serial data by ORing P_INVERT_IN into the P_ASYNC_RX mode word.
- **Correct (true fact):** The async receiver samples the A input. The A-input polarity is inverted by the %AAAA invert bit = P_INVERT_A. P_INVERT_IN inverts the low-level IN bit (used for logic/schmitt pin reads); in smart-pin async-RX mode IN signals 'data ready', so P_INVERT_IN does not invert the received data. Correct constant is P_INVERT_A.
- **Source proof:** Silicon Doc v35 p2-documentation.txt L7573-7615 (%AAAA 'A input selector: 1xxx = inverted'; '%FFF ... after A and B input selectors'; 'resultant A drives IN in non-smart-pin modes') + L9156-9162 (%11111 async RX: 'serially received on the A input'); Spin2 v55 spin2-v55-text.txt L1423 (P_INVERT_A = '

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-17-serial-receive | For RS-232 with external level shifter, invert the received serial data by ORing → Use P_INVERT_A to invert the received (A-input) serial data: PINSTART(RX_PIN, P_ |
| IOSP | part-3-input-modes/chapter-17-serial-receive | P_INVERT_IN inverts the (received serial) input, for RS-232. → Row should read 'P_INVERT_A \| Invert received serial data (A input) — e.g. RS-2 |

## C-38: `y-count-range-off-by-one` — 2 sites · IOSP

- **The defect:** The P_PULSE cycle count range is 1 to 2³².
- **Correct (true fact):** Y[31:0] is a 32-bit field; its maximum value is 2³²−1 (4,294,967,295), not 2³².
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt line 326 (Y[31:0] is 32-bit); a 32-bit unsigned register holds 0..2³²−1.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §7.8 Quick Reference, P_PULSE Configuration  | The P_PULSE cycle count range is 1 to 2³². → Cycle count range is 1 to 2³²−1 (a 32-bit value; 0 does not trigger). |
| IOSP | §7.8 Quick Reference, P_TRANSITION Configura | The P_TRANSITION edge count range is 1 to 2³². → Edge count range is 1 to 2³²−1. |

## C-39: `abs-neg-idiom-computes-identity` — 1 site · Assembly (Part I)

- **The defect:** abs result,value wc / if_c neg result presented as a branchless, 'edge-case safe' absolute value.
- **Correct (true fact):** Because ABS sets C = original sign (C=1 for ALL negatives), 'if_c neg result' negates the just-computed magnitude back to negative for every negative input. E.g. value=-5: abs→5,C=1; if_c neg→-5. The sequence returns the ORIGINAL value (identity), not \|value\|.
- **Source proof:** v35 CSV row 62 (ABS c=S[31]) + row 64 (NEG: 'D = -D. C = MSB of result.')

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.5.4 lines 424-439 (co | abs result,value wc / if_c neg result presented as a branchless, 'edge-case safe → A correct branchless abs is 'abs result, value' alone (2 clk). The abs+`if_c neg |

## C-40: `adc-ext-edge-vs-rise` — 1 site · IOSP

- **The defect:** Samples A-input data on B-input clock edges
- **Correct (true fact):** In the externally-clocked mode, the A-input is sampled on each B-input RISE (rising edge only), not on both edges.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 811-813 / p2-documentation.txt %11001

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-f-mode-reference. | Samples A-input data on B-input clock edges → Samples A-input data on each B-input rising edge. |

## C-41: `adc-gio-calibration-not-signal-input` — 1 site · IOSP

- **The defect:** P_ADC_GIO configures the ADC to read a ground-referenced single-ended signal from the pin.
- **Correct (true fact):** P_ADC_GIO routes the ADC to the internal GIO (ground) calibration source, not to the pin's external signal; it measures ground (~0) for calibration.
- **Source proof:** Spin2 v55 line 1466: 'P_ADC_GIO \| ADC GIO → IN'; Silicon Doc p2-documentation.txt line 452: 'Delta-sigma ADC with 5 ranges, 2 sources, and VIO/GIO calibration'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-e-troubleshooting | P_ADC_GIO configures the ADC to read a ground-referenced single-ended signal fro → To read an external single-ended signal, select a gain range (e.g. P_ADC_1X \| P |

## C-42: `adc-input-select-wrong` — 1 site · DeSilva

- **The defect:** ADC continuous-sampling of an analog signal is configured with wrpin ##P_ADC \| P_ADC_GIO
- **Correct (true fact):** P_ADC_GIO routes the ADC to the internal GIO (group ground reference), used for calibration; P_ADC_1X routes the pin's own external input at 1x gain
- **Source proof:** spin2-v55 L1466 P_ADC_GIO='ADC GIO → IN'; L1469 P_ADC_1X='ADC 1x → IN'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch14 'ADC Input' li | ADC continuous-sampling of an analog signal is configured with wrpin ##P_ADC \|  → To sample the pin's external analog signal use wrpin ##P_ADC \| P_ADC_1X, #ADC_P |

## C-43: `adc-scope-four-channel-overstate` — 1 site · IOSP

- **The defect:** P_ADC_SCOPE is a four-channel oscilloscope-style ADC
- **Correct (true fact):** The %11010 mode calculates an 8-bit ADC sample and checks hysteretic triggering for ONE pin, providing oscilloscope functionality; samples from blocks of UP TO four pins can be grouped into the 32-bit SCOPE data pipe. The single-pin mode is one channel; four channels is a cog-level SCOPE-data-pipe aggregate, not a property of this one mode.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 8770-8775

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-f-mode-reference. | P_ADC_SCOPE is a four-channel oscilloscope-style ADC → Single-channel triggered oscilloscope-style ADC per pin, with hysteretic trigger |

## C-44: `adc-scope-pin-alignment-fabrication` — 1 site · IOSP

- **The defect:** For P_ADC_SCOPE the pin must be a multiple of 4
- **Correct (true fact):** The %11010 scope mode computes an 8-bit sample and checks hysteretic triggering on any pin; the sample is read with RDPIN/RQPIN. Only the optional SCOPE data pipe (SETSCP, D[5:2] selects the 4-pin block; GETSCP) is aligned to blocks of 4 pins. Nothing requires the scope-mode pin itself to be a multiple of 4.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 8770-8775, 8816-8828 (SCOPE mode + SCOPE Data Pipe / SETSCP)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-f-mode-reference. | For P_ADC_SCOPE the pin must be a multiple of 4 → Any pin may use scope mode; a multiple-of-4 alignment matters only if you aggreg |

## C-45: `address-width-32-vs-20-bit` — 1 site · DeSilva

- **The defect:** jmp #\far_away — '\ forces a 32-bit absolute address'
- **Correct (true fact):** P2 branch address fields are 20-bit (D[19:0]/A[19:0]); the '\' after '#' forces absolute (R=0) addressing, and the absolute address is 20-bit, giving a 1MB execution space.
- **Source proof:** v35 CSV row 402 (JMP #{\}A): encoding EEEE 1101100 RAA... = 20-bit A field; '\' forces R=0. Silicon Doc lines 664-665 ('20-bit Address field is absolute'), 683, 1293, 1532.

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.10 'Long Jumps an | jmp #\far_away — '\ forces a 32-bit absolute address' → The '\' forces a 20-bit ABSOLUTE (non-relative) hub address, not a 32-bit addres |

## C-46: `addressing-mode-overgeneralization` — 1 site · DeSilva

- **The defect:** Symmetry: Every instruction can use every addressing mode
- **Correct (true fact):** Addressing modes are NOT uniform across the instruction set: hub RD/WR instructions use S/#/PTRx forms, branch instructions use 20-bit relative/absolute addresses, no-operand instructions have no addressing, and many instructions accept only specific operand forms.
- **Source proof:** Silicon Doc v35 p2-documentation.txt L6913-6925 (hub instructions have their own S/#/PTRx addressing set, distinct from ALU ops) and L6851-6868 (RDxxx/WRxxx differ from register-to-register ops); branch instructions use 20-bit addresses

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md, Ch.3 sidetrack 'Why | Symmetry: Every instruction can use every addressing mode → PASM2 is unusually regular, but not literally 'every instruction can use every a |

## C-47: `adds-subs-true-sign-vs-result-bit31` — 1 site · Assembly (Part I)

- **The defect:** ADDS and SUBS set C to the true sign of the result (result bit 31).
- **Correct (true fact):** C is the CORRECTED (full-precision) sign of D±S, which on signed overflow DIFFERS from the stored result's bit 31 — that is the whole point of the S variants.
- **Source proof:** v35 CSV row 12 ADDS 'C = correct sign of (D + S)'; row 16 SUBS 'C = correct sign of (D - S)'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.4.1 line 295 | ADDS and SUBS set C to the true sign of the result (result bit 31). → Delete the '(result bit 31)' gloss: ADDS/SUBS set C to the corrected/full-precis |

## C-48: `alias-set-membership-undercount` — 1 site · IOSP

- **The defect:** Spin2 also accepts short-form aliases for the three most common of these: PINH for PINHIGH, PINL for PINLOW, and PINF for PINFLOAT.
- **Correct (true fact):** Spin2 defines SIX short-form pin-method aliases — PINW(PINWRITE), PINL(PINLOW), PINH(PINHIGH), PINT(PINTOGGLE), PINF(PINFLOAT), PINR(PINREAD) — not three. PINTOGGLE, PINWRITE, and PINREAD also have short forms.
- **Source proof:** Spin2 v55 text lines 531-536 (Pin Methods table): PINW, PINL, PINH, PINT, PINF, PINR

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §1.8 intro, line 986 | Spin2 also accepts short-form aliases for the three most common of these: PINH f → Spin2 accepts short-form aliases for six pin methods: PINW, PINL, PINH, PINT, PI |

## C-49: `alignl-8byte-vs-4byte-long` — 1 site · DeSilva

- **The defect:** 'Align branch targets to 8-byte boundaries' followed by 'alignl ' Align to long boundary'
- **Correct (true fact):** ALIGNL aligns to a LONG (4-byte) boundary; there is no 8-byte alignment directive (ALIGNW=2-byte word, ALIGNL=4-byte long).
- **Source proof:** Spin2 v55 ref line 305: 'ALIGNL long-align to hub by emitting 1 to 3 zero bytes'; line 268 'ALIGNL long-align'. ALIGNW = word-align (2 bytes), ALIGNL = long-align (4 bytes).

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.10 'Performance O | 'Align branch targets to 8-byte boundaries' followed by 'alignl ' Align to long  → 'Align branch targets to long (4-byte) boundaries' — alignl produces 4-byte alig |

## C-50: `alt-modifier-reversal-mischaracterization` — 1 site · Debug Window

- **The defect:** ALT: swap adjacent same-width fields ... not a reversal
- **Correct (true fact):** The ALT keyword will cause bits, double-bits, or nibbles, within each byte sent, to be reordered END-TO-END on the host side, within each byte.
- **Source proof:** Spin2 v55 Language Reference line 1403 (Packed-Data Modes, ALT keyword)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | appendix-b-packed-data.md § Modifiers, line  | ALT: swap adjacent same-width fields ... not a reversal → ALT reorders the same-width sub-fields end-to-end (i.e. reverses their order) wi |

## C-51: `alt-modifier-scope-overstatement` — 1 site · Debug Window

- **The defect:** ALT: swap ... fields throughout the container
- **Correct (true fact):** reordering happens WITHIN EACH BYTE SENT, stated twice; it does not cross byte boundaries.
- **Source proof:** Spin2 v55 Language Reference line 1403 (ALT keyword: 'within each byte sent ... within each byte')

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | appendix-b-packed-data.md § Modifiers, line  | ALT: swap ... fields throughout the container → ALT reorders sub-fields within each byte, not across the whole container; for wo |

## C-52: `any-edge-double-counts-frequency` — 1 site · IOSP

- **The defect:** With Y=%11 ("Any edge") and X=1000 edges, frequency = MULDIV64(sysclk, 1000, period).
- **Correct (true fact):** 'Any edge' sensitivity counts BOTH the rising and falling transition of each cycle — two events per period. Timing 1000 any-edges therefore spans 500 signal periods, so signal frequency = sysclk*500/period, i.e. MULDIV64(sysclk, 500, period).
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 683-693: %10010 !Y[2], Y[1:0] %1x = 'A-input edge' (any edge).

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-13-timing-measurement.md §13.7 Examp | With Y=%11 ("Any edge") and X=1000 edges, frequency = MULDIV64(sysclk, 1000, per → For any-edge counting divide the edge count by two: frequency = MULDIV64(sysclk, |

## C-53: `async-fractional-baud-condition-omitted` — 1 site · IOSP

- **The defect:** With fractional precision: bit_period_frac := MULDIV64(_clkfreq, 65536, baud); X_value := (bit_period_frac & $FFFFFC00) \| (data_bits - 1) — presented as a generally usable fractional-baud technique, with X[15:10] documented as the fractional field.
- **Correct (true fact):** 'X[31:16] establishes the number of clocks in a bit period, and in case X[31:26] is zero, X[15:10] establishes the number of fractional clocks.' The fractional field is ONLY honored when X[31:26]==0 — i.e. when the integer bit period is < 1024 clocks. For every baud rate in the doc's own 200 MHz table (9600->20833 clocks, ... 921600->217 clocks) except the very fastest, X[31:26] is non-zero, so th
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 9159-9161 (%11111 async receive WXPIN)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §17.2 Baud Rate Calculation, With fractional | With fractional precision: bit_period_frac := MULDIV64(_clkfreq, 65536, baud); X → State that fractional-clock precision (X[15:10]) is applied by the smart pin onl |

## C-54: `async-stopbit-validation-fabrication` — 1 site · IOSP

- **The defect:** The smart pin monitors for a high-to-low transition (start bit), samples data bits at mid-bit timing, and validates the stop bit.
- **Correct (true fact):** The async-receive state machine waits for start edge, delays half a bit period, samples each data bit at one-bit-period intervals, then 'Capture the shifter into the Z register and raise IN' and loops. There is NO stop-bit sampling or validation step; the hardware never checks that the stop bit is high.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 9156-9194 (%11111 async receive internal state sequence, steps 1-8)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §17.2 P_ASYNC_RX Operation, line 34 | The smart pin monitors for a high-to-low transition (start bit), samples data bi → ...samples each data bit at mid-bit timing, then captures the word and raises IN |

## C-55: `async-tx-wait-before-first-write` — 1 site · IOSP

- **The defect:** Enable the async-TX pin, then wait for IN (REPEAT UNTIL PINREAD) BEFORE the first WYPIN
- **Correct (true fact):** Async TX step 1 waits for an output word to be buffered via WYPIN; IN is first raised at step 2, AFTER a word has been written. During reset IN is low. So IN is not raised until the first WYPIN — waiting for IN before the first WYPIN never completes.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 9098-9105 (async TX internal state sequence)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-f-mode-reference. | Enable the async-TX pin, then wait for IN (REPEAT UNTIL PINREAD) BEFORE the firs → For an output mode, WYPIN the first byte first, then REPEAT UNTIL PINREAD(pin) b |

## C-56: `aug-intervening-instruction-loss` — 1 site · Assembly (Part I)

- **The defect:** The AUG instruction must immediately precede the instruction it augments; if any instruction intervenes (including a conditional NOP), the augmentation is lost.
- **Correct (true fact):** Silicon Doc: intervening instructions between AUGS and its intended target do NOT cancel the augment ('will use the AUGS value, but not cancel it'); the augment is consumed by the next instruction that has the matching immediate #S (AUGS) / #D (AUGD). CSV AUGS: 'Queue #n ... for next #S occurrence.'
- **Source proof:** Silicon Doc p2-documentation.txt lines 211-227; CSV row 408 AUGS ('for next #S occurrence')

TODO: this sounds suspicious/incorrect... any more proof sources?

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.7.3 Augm | The AUG instruction must immediately precede the instruction it augments; if any → AUGS/AUGD attach to the NEXT instruction that has a matching immediate operand ( |

## C-57: `backslash-absolute-address-wording` — 1 site · Assembly (Part I)

- **The defect:** #\label is an 'Absolute Cog-relative address' that 'Forces 9-bit Cog address'
- **Correct (true fact):** The \ prefix forces the operand to be treated as an absolute address (suppressing relative/AUGS optimization). 'Absolute' and 'relative' are mutually exclusive, so 'Absolute Cog-relative address' is self-contradictory terminology.
- **Source proof:** pnut-ts v1.55.0: `call #\.helper` compiles; the backslash forces absolute (non-PC-relative) addressing

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.10.3 Lab | #\label is an 'Absolute Cog-relative address' that 'Forces 9-bit Cog address' → #\label forces the assembler to use the label's absolute address (rather than a  |

## C-58: `baud-divisor-round-vs-truncate` — 1 site · IOSP

- **The defect:** The X[31:16] integer divisor for 19200 baud at 200 MHz is 10417
- **Correct (true fact):** The stated integer formula (Spin2 integer division truncates) yields floor(10416.667)=10416, not 10417. Every other row in the table uses truncation; 19200 is the only row rounded up.
- **Source proof:** Doc §11.2 line 52 (its own 'Basic formula, integer only'): X[31:16] = sysclk / baud_rate; and worked example line 55 uses truncation (200e6/115200=1736). 200,000,000 / 19200 = 10416.667.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | The X[31:16] integer divisor for 19200 baud at 200 MHz is 10417 → 19200 \| 10416 (per the stated sysclk/baud integer formula) — or note that the t |

## C-59: `baud-error-numeric` — 1 site · IOSP

- **The defect:** Integer-only bit period gives 0.02% error at 115200 baud
- **Correct (true fact):** Integer-only error at 115200 baud/200MHz is ~0.0064% (rounds to 0.01%), not 0.02%.
- **Source proof:** Arithmetic from doc's own formula (line 514): round(200_000_000/115200)=1736; actual=200_000_000/1736=115207.37; error=7.37/115200=0.0064% → 0.01%.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | Integer-only bit period gives 0.02% error at 115200 baud → Integer only \| 1 clock \| ~0.01% (≈0.006%) |

## C-60: `baud-table-rounding-vs-truncation` — 1 site · IOSP

- **The defect:** 19200 baud => 10417 clocks/bit => X[31:16] = $28B1
- **Correct (true fact):** Integer division (the operation the doc's Spin2/PASM examples actually perform) truncates 10416.67 to 10416 = $28B0. The table lists the rounded value 10417 = $28B1, inconsistent with the doc's stated formula. Every other row in the table matches truncation; only 19200 is rounded up.
- **Source proof:** Arithmetic: 200_000_000 / 19200 = 10416.67; the doc's own formula bit_period := _clkfreq / BAUD (line 98, integer division) yields 10416, not 10417. $28B1 = 10417.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §17.2 Common baud rates at 200 MHz table, li | 19200 baud => 10417 clocks/bit => X[31:16] = $28B1 → 19200 -> 10416 clocks/bit -> $28B0 (to match the doc's integer-division formula) |

## C-61: `bit-count-off-by-one` — 1 site · IOSP

- **The defect:** or  x_val, #8   (setting X[4:0]=8 in an '8 data bits' async-TX config)
- **Correct (true fact):** X[4:0] = N-1. For 8 data bits write 7. Writing 8 selects a 9-bit word.
- **Source proof:** Silicon-doc p2-documentation.txt async-serial-transmit: 'X[4:0] sets the number of bits, minus 1. For example, a value of 7 will set the word size to 8 bits.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | or  x_val, #8   (setting X[4:0]=8 in an '8 data bits' async-TX config) → or  x_val, #7   ' 8 data bits (X[4:0] = N - 1) |

## C-62: `block-transfer-exceeds-cog-ram` — 1 site · DeSilva

- **The defect:** 'Copy 1000 longs (4KB) at maximum speed' via setq ##1000-1 then rdlong buffer, source ('Read them all!'), then setq ##1000-1 / wrlong buffer, dest.
- **Correct (true fact):** SETQ+RDLONG performs a cog/LUT block transfer whose destination D is a cog register; cog register RAM is only 512 longs. A 1000-long block read into cog starting at 'buffer' overruns the 512-long cog register file (wrapping and clobbering code/registers). 1000 longs cannot be held in a single cog's register space.
- **Source proof:** v35 CSV row 337 (SETQ 'Set Q to D. Use before RDLONG/WRLONG...to set block transfer') + row 154 (RDLONG D = cog register destination); Silicon Doc COG-RAM-REGISTER-MAP / hub-ram-section: cog register RAM = 512 longs

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Ch.9 §The Hook: 4KB in 4 Instructions, line  | 'Copy 1000 longs (4KB) at maximum speed' via setq ##1000-1 then rdlong buffer, s → SETQ block reads land in cog (or LUT) registers, which hold at most 512 longs, s |

## C-63: `boot-pin-mapping-swap` — 1 site · Assembly (Part I)

- **The defect:** For SD card boot: P61 = Chip Select (active low), P60 = Clock.
- **Correct (true fact):** For SD card boot the pins map P61=CLK (clock), P60=CSn (chip select), P59=DI, P58=DO — the CLK and CSn are SWAPPED relative to SPI flash (SPI: P61=CSn, P60=CLK).
- **Source proof:** Silicon Doc p2-documentation.txt lines 9275-9300 (Boot Memory / SD card): pin columns P61,P60,P59,P58; SD-card row = CLK, CSn, DI, DO

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.7.3 SD Card Boot t | For SD card boot: P61 = Chip Select (active low), P60 = Clock. → For SD card boot: P61 = Clock (output), P60 = Chip Select / CSn (output), P59 =  |

## C-64: `boot-table-dontcare-overspecified` — 1 site · Assembly (Part I)

- **The defect:** The 'serial 100ms then SPI flash' boot mode requires P61=pull-up, P60=none, P59=none.
- **Correct (true fact):** For the SPI-flash boot rows the silicon marks P60 as 'ignored' (don't-care), not 'none'. Only P61 and P59 determine SPI boot behavior.
- **Source proof:** Silicon Doc p2-documentation.txt lines 9223-9235 (Boot Pattern table): 'Serial 100ms then SPI flash' = P61 pull-up, P60 IGNORED, P59 none; 'SPI flash only fast boot' = P61 pull-up, P60 IGNORED, P59 pull-down

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.7.2 Boot Source Se | The 'serial 100ms then SPI flash' boot mode requires P61=pull-up, P60=none, P59= → P60 is a don't-care ('ignored'/'any') for the SPI-flash boot rows; listing it as |

## C-65: `c-flag-mode-meaning-fabrication` — 1 site · IOSP

- **The defect:** For Serial RX modes, the RDPIN/RQPIN C flag means 'Parity or error'.
- **Correct (true fact):** The async serial receive mode (%11111) 'Words from 1 to 32 bits are serially received... Capture the shifter into the Z register and raise IN' — there is NO parity feature and no error/parity flag anywhere in the mode description. General rule: C receives a mode-related flag or the MSB of the Z result. P2 smart-pin serial has no hardware parity.
- **Source proof:** Silicon Doc p2-documentation.txt L9156-9194 (%11111 async serial receive) and part4-smart-pins.txt L1-3 (C = mode-related flag or MSB of Z)

TODO: do we have to be careful here with rdpin() (spin2) vs. rdpin (pasm2)?  rdpin() spin2 C bit encoding is special

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-04-smart-pin-configuration.md §4.12  | For Serial RX modes, the RDPIN/RQPIN C flag means 'Parity or error'. → For serial RX modes the C flag carries the modal result (typically the MSB of th |

## C-66: `clock-config-example-broken` — 1 site · Assembly (Part I)

- **The defect:** hubset ##%...0001_0010 ' Enable xtal / hubset ##...0010_0010 ' Switch
- **Correct (true fact):** Low byte PPPP_CCSS: value1 %0001_0010 => SS=%10 (XI selected immediately) and CC=%00 (XI ignored/float, Hi-Z, caps off — crystal NOT enabled, E=0 so PLL off). The silicon canonical 'enable' step keeps SS=%00 (current source) while setting CC=%10 and E=1; only the final step sets SS=%11/%10.
- **Source proof:** Silicon Doc v35 lines 6120-6260 (HUBSET field map + canonical PLL example)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.1.4 Clock Switching  | hubset ##%...0001_0010 ' Enable xtal / hubset ##...0010_0010 ' Switch → The 'enable' HUBSET must set CC to a non-zero XI-loading value (e.g. %10) and ke |

## C-67: `clock-config-hubset-encoding` — 1 site · Assembly (Part I)

- **The defect:** The HUBSET immediate values shown configure a 20 MHz crystal with PLL for 160 MHz (divide/1, multiply 8, post/1), enabling 15pF crystal caps.
- **Correct (true fact):** In the documented HUBSET clock format the PLL-enable bit is bit24, DDDDDD[23:18]=divider-1, MMMMMMMMMM[17:8]=multiplier-1, PPPP[7:4]=post-divider select (%1111=VCO direct), [3:2]=pin/cap mode (%10=15pF), [1:0]=clock source (%00=stay RCFAST, %11=PLL). A 20MHz->160MHz config is div/1 (DDDDDD=0), x8 (MMMM=7), PPPP=%1111.
- **Source proof:** Silicon Doc p2-documentation.txt lines 6250-6262 (Configuring the Clock Generator): config value format %1_DDDDDD_MMMMMMMMMM_PPPP_XX_CC, enable bit is bit24; worked example %1_100111_0100101000_1111_10_11

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.7.6 clock-config e | The HUBSET immediate values shown configure a 20 MHz crystal with PLL for 160 MH → The shown values do not implement 20MHz->160MHz. As written each value is only 2 |

## C-68: `clock-failure-fallback-fabrication` — 1 site · Assembly (Part I)

- **The defect:** The P2 provides automatic fallback to RCFAST if the selected clock source fails, preventing system lockup from clock problems.
- **Correct (true fact):** "Incorrectly switching away from the PLL setting ... can cause a clock glitch which will hang the P2 chip until a reset occurs." No automatic clock-failure detection or fallback-to-RCFAST mechanism exists anywhere in the clock-generator section.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 6228-6229 (Clock Config WARNING)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.1.4 Clock Switching  | The P2 provides automatic fallback to RCFAST if the selected clock source fails, → RCFAST is only the power-on/reset default source; the P2 has no runtime clock-fa |

## C-69: `clock-halfperiod-labeling` — 1 site · IOSP

- **The defect:** WXPIN for P_TRANSITION clock sets the 'Clock period'
- **Correct (true fact):** For P_TRANSITION the WXPIN value is the clocks-per-transition = half-period, not the full clock period. The doc's own §11.4 and line 405 (SPI_PERIOD=50 → 2 MHz = 100 clocks/full-cycle) confirm the half-period reading.
- **Source proof:** Silicon Doc p2-documentation.txt (%00101 P_TRANSITION): X[15:0] = base period in clock cycles per transition (half a full clock cycle); Doc §11.4 line 319 (its own): 'WXPIN(CLK_PIN, period)  ' Clocks per half-period'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | WXPIN for P_TRANSITION clock sets the 'Clock period' → ' Clock half-period (clocks per transition) |

## C-70: `clock-spec-max-overstated` — 1 site · P2AN004

- **The defect:** These programs run at 200 MHz. The P2's specified maximum is 300 MHz; there is no reason to overclock for any of these measurements
- **Correct (true fact):** The silicon doc gives no '300 MHz specified maximum'. It states the VCO is designed for 100-200 MHz (so ~200 MHz is the intended sysclock ceiling) and that overclocking can push the PLL to 350 MHz. 300 MHz falls in overclock territory, not a specified maximum.
- **Source proof:** Silicon Doc p2-documentation.txt line 6143 ('the PLL can be pushed to 350 MHz using the VCO/1 mode') and line 6233 ('The PLL's VCO is designed to run between 100 MHz and 200 MHz and should be kept within that range').

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN004 | P2AN004.md §Pitfalls & Notes, 'stay at a leg | These programs run at 200 MHz. The P2's specified maximum is 300 MHz; there is n → Rephrase to match a citable spec: the P2's PLL VCO is designed for 100-200 MHz ( |

## C-71: `cog-exec-timing-overgeneralization` — 1 site · DeSilva

- **The defect:** Cog Execution (traditional): Fast: exactly 2 clocks per instruction
- **Correct (true fact):** In cog-execution mode most register-to-register ALU ops take 2 clocks, but a taken branch takes at least 5 clocks (pipeline flush) and a random hub access (RDLONG/WRLONG) takes 9-16 clocks; CORDIC/QMUL vary (2...9). Instruction timing is NOT uniformly 2 clocks.
- **Source proof:** Silicon Doc v35 L631-632 (branch = at least 5 clocks); CSV RDLONG cog-clocks 9...16; same-doc L3199 'Random hub access: 9-16 clocks per access'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md ch.10 'Cog vs Hub Ex | Cog Execution (traditional): Fast: exactly 2 clocks per instruction → Cog execution runs most simple instructions in 2 clocks, but hub-access instruct |

## C-72: `cog-ram-address-range-error` — 1 site · DeSilva

- **The defect:** In 'mov value, $200', $200 is a cog RAM address (so it reads cog RAM, not LUT).
- **Correct (true fact):** Cog register (cog RAM) address space is $000..$1FF (512 longs). $200 is outside cog RAM; a 9-bit register operand cannot encode it — pnut-ts rejects 'mov value, $200' with 'Register cannot exceed $1FF'. In the cog PC/execution space $200..$3FF is the LUT range, not cog RAM.
- **Source proof:** Silicon Doc line 983 (RDLUT/WRLUT addressable $000..$1FF), lines 595/605 cog registers $000..$1FF; pnut-ts v1.55: 'mov value, $200' → error 'Register cannot exceed $1FF'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.13 'Common Gotcha | In 'mov value, $200', $200 is a cog RAM address (so it reads cog RAM, not LUT). → Cog RAM registers are $000..$1FF; $200 is not a cog RAM address (it exceeds the  |

## C-73: `cog-start-always-overgeneralization` — 1 site · DeSilva

- **The defect:** Cogs always start executing at (cog) address 0
- **Correct (true fact):** For register/cog-exec loads the cog begins at cog address $000, but for hub-exec starts (COGEXEC vs HUBEXEC / the +32 mode bit) the cog begins executing at the HUB address supplied to COGINIT — so 'Always start at 0' is not universally true.
- **Source proof:** Spin2 v55 text line 320: hub-exec COGINIT(32+16, @IncPins, 0) begins execution at the hub address ($00404 in the example), not cog $000; line 311 shows the cog-exec case starting at cog $000

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Chapter 2, 'Common Gotchas' item 2, line 813 | Cogs always start executing at (cog) address 0 → A cog loaded with a cog-exec (COGEXEC) program begins at cog address $000; a hub |

## C-74: `cogatn-mask-width` — 1 site · DeSilva

- **The defect:** The COGATN instruction takes an 8-bit mask where each bit corresponds to a cog. Setting bit N sends attention to Cog N.
- **Correct (true fact):** COGATN's operand is a 16-bit mask (D[15:0]); bits 0..15 represent cogs 0..15. The attention-strobe network has 16 strobes.
- **Source proof:** v35 CSV row 340 (COGATN): 'Strobe attention of all cogs whose corresponding bits are high in D[15:0].'; Silicon Doc p2-documentation.txt line 5078-5080: 'The D/# operand supplies a 16-bit value in which bits 0..15 represent cogs 0..15 ... 16 attention strobe outputs'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | §'ATN - Inter-Cog Events', COMPLETE-OPUS-MAS | The COGATN instruction takes an 8-bit mask where each bit corresponds to a cog.  → COGATN takes a 16-bit mask in D[15:0]; each set bit N strobes cog N (cogs 0..15) |

## C-75: `coginit-ptra-ptrb-swap` — 1 site · Assembly (Part I)

- **The defect:** COGINIT '...optionally passes a parameter to the new cog. The parameter value appears in the new cog's PTRB register, providing a simple mechanism for initialization data.'
- **Correct (true fact):** The code/start ADDRESS (S) is written to PTRB. The optional runtime parameter (initialization data, passed via a preceding SETQ) is written to PTRA — NOT PTRB.
- **Source proof:** v35 CSV row 234 (COGINIT): 'S[19:0] sets hub startup address and PTRB of cog. Prior SETQ sets PTRA of cog.'; Silicon Doc p2-documentation.txt lines 795-800: S value 'written into the target cog's PTRB register... If COGINIT is preceded by SETQ, the SETQ value will be written into the target cog's PT

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-01-execution-model.md §1.1.3 line 41 | COGINIT '...optionally passes a parameter to the new cog. The parameter value ap → The code/start address is written to the new cog's PTRB register; an optional pa |

## C-76: `coginit-ptrb-code-pointer-not-user-param` — 1 site · DeSilva

- **The defect:** rdlong delay, ptrb reads a per-cog 'Different delay per cog' value from PTRB after COGINIT
- **Correct (true fact):** COGINIT passes exactly ONE user value (3rd arg) into PTRA. PTRB is loaded with the CODE pointer (the @address / PASMaddr, 2nd arg), not a user-supplied delay. There is no second parameter slot for a delay.
- **Source proof:** Spin2 v55 text line 360 (special-register table): PTRA = 'Data pointer passed from COGINIT', PTRB = 'Code pointer passed from COGINIT'; line 517: COGINIT(CogNum, PASMaddr, PTRAvalue)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Chapter 2, 'Your Turn: Experiment 2 Parallel | rdlong delay, ptrb reads a per-cog 'Different delay per cog' value from PTRB aft → COGINIT delivers only one parameter, into PTRA; PTRB holds the code's load addre |

## C-77: `color-name-lime-vs-green` — 1 site · Debug Window

- **The defect:** TERM default color pair 2 foreground and pair 3 background are 'Lime'
- **Correct (true fact):** The default TERM color-scheme constant for pairs 2 and 3 is GREEN; 'LIME' is not among the recognized Spin2 DEBUG color names.
- **Source proof:** Spin2 v55 spin2-v55-text.txt:1306 — TERM Instantiation COLOR default: '0 = ORANGE/BLACK 1 = BLACK/ORANGE 2 = GREEN/BLACK 3 = BLACK/GREEN'; valid DEBUG color names (line 1320) are BLACK/WHITE/ORANGE/BLUE/GREEN/CYAN/RED/MAGENTA/YELLOW/GRAY

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | appendix-c-color-coordinate.md §TERM color p | TERM default color pair 2 foreground and pair 3 background are 'Lime' → Pair 2 foreground and Pair 3 background are GREEN (the Spin2 named constant used |

## C-78: `compare-field-mislabel-hightime-vs-lowtime` — 1 site · IOSP

- **The defect:** A constant named STEP_HIGH (=200, '1 µs high time') is placed into X[31:16] via `WXPIN(STEP_PIN, STEP_PERIOD \| (STEP_HIGH << 16))`.
- **Correct (true fact):** X[31:16] holds the LOW-time (compare) clocks; high time = X[15:0] − X[31:16]. A value placed in X[31:16] sets the low time, not the high time.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 321-323; and this doc's own line 52 / line 410: X[31:16] is the compare value = LOW-time clocks (output HIGH while counter > X[31:16]).

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §7.7 Example 1 (Stepper Motor Step Pulse), l | A constant named STEP_HIGH (=200, '1 µs high time') is placed into X[31:16] via  → The value written to X[31:16] is the LOW-time / compare value (as line 94 correc |

## C-79: `concurrent-pin-sync-race` — 1 site · IOSP

- **The defect:** Waiting only on SIG_PIN's IN flag is safe because both pins finish on the same edge, so SIG_PIN+1's result is already latched.
- **Correct (true fact):** Each smart pin begins its period count on its own first trigger after DIRH. The two pins are enabled by two sequential PINSTART calls; if a signal edge falls between them, the pins start one period apart and complete one edge apart. §15.4 (line 271) instead waits on ALL pins with `REPEAT UNTIL PINREAD(A) AND PINREAD(B) AND PINREAD(C)`.
- **Source proof:** Silicon Doc part4-smart-pins.txt lines 749-756 (measurement begins on first A-rise/edge trigger after enable); doc's own §15.4 line 271

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §15.2 duty example, line 141 | Waiting only on SIG_PIN's IN flag is safe because both pins finish on the same e → Prefer waiting on all measurement pins (AND of each PINREAD, as in §15.4) rather |

## C-80: `conditional-exec-timing-overgeneralization` — 1 site · DeSilva

- **The defect:** Any instruction can carry a condition prefix and still take exactly 2 clocks
- **Correct (true fact):** Instruction clock counts vary widely: simple ALU ops are 2 clocks, but hub ops (RDLONG 9-16), CORDIC reads (GETQX/GETQY 2...58) and others are not. A condition prefix does not add clocks or flush the pipeline, but it does not make every instruction a 2-clock instruction.
- **Source proof:** v35 CSV: RDLONG cog clocks '9...16'; GETQX row 258 '2...58'; MUL row 137 '2'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch6 medicine-cabinet | Any instruction can carry a condition prefix and still take exactly 2 clocks → A condition prefix adds no clocks and causes no pipeline flush; a simple ALU ins |

## C-81: `config-bitfield-range-misassignment` — 1 site · IOSP

- **The defect:** Layer 3: Input Routing (bits [31:24]) ... Input polarity: true or inverted; Input logic: pass, AND, OR, XOR, or filter
- **Correct (true fact):** The WRPIN D operand packs %AAAA (bits31:28, A source+polarity), %BBBB (bits27:24, B source+polarity), then %FFF (bits23:21) = 'A and B input logic/filtering' selecting A,B / AND / OR / XOR / filt0-3. The A/B input SELECTORS+polarity are bits [31:24]; the input-logic/filter selection (pass/AND/OR/XOR/filter) is FFF at bits [23:21], NOT within [31:24].
- **Source proof:** Silicon Doc part4-smart-pins.txt WRPIN format line 10 (%AAAA_BBBB_FFF_M...M_TT_SSSSS_0) + lines 39-47 (FFF = A/B input logic/filtering) ; full-doc p2-documentation.txt:7865-7866

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-1-fundamentals/chapter-03-smart-pin-arc | Layer 3: Input Routing (bits [31:24]) ... Input polarity: true or inverted; Inpu → Layer 3: Input Routing occupies bits [31:21] — A/B input source selection and po |

## C-82: `constant-overflow-misattribution` — 1 site · P2AN002

- **The defect:** "...STEPS equal steps are 2^32 / STEPS apart. That value would overflow a 32-bit constant written directly, so it is formed as $8000_0000 / (STEPS / 2)"
- **Correct (true fact):** The step VALUE (2^32/STEPS = 2^26 for STEPS=64) is only 27 bits and fits a 32-bit constant. What actually overflows is the dividend literal $1_0000_0000 (2^32, 33 bits) if written directly.
- **Source proof:** pnut_ts v1.55.0 compile test: `$1_0000_0000 / STEPS` => error 'Constant exceeds 32 bits'; quotient 2^32/64 = $0400_0000 (27 bits) compiles fine.

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN002 | P2AN002.md §Recipe 3 'How this works', line  | "...STEPS equal steps are 2^32 / STEPS apart. That value would overflow a 32-bit → The quotient itself fits fine; the reason for the workaround is that the DIVIDEN |

## C-83: `control-instruction-timing-range` — 1 site · Assembly (Part I)

- **The defect:** 'Hub control instructions (HUBSET, COGINIT, LOCK*, CORDIC) have different timing of 2-9 clocks.'
- **Correct (true fact):** Most named hub-control ops are 2...9 clocks, but LOCKNEW — a member of the globbed set 'LOCK*' — is 4...11 clocks in cog/LUT mode, exceeding the stated 2-9 range.
- **Source proof:** v35 CSV: HUBSET row 241 (2...9), COGINIT row 234 (2...9), LOCKRET/LOCKTRY/LOCKREL rows 245-247 (2...9), CORDIC Q* rows 235-249 (2...9), BUT LOCKNEW row 244 = 4...11 (cog/LUT).

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-01-execution-model.md §1.4.2 line 14 | 'Hub control instructions (HUBSET, COGINIT, LOCK*, CORDIC) have different timing → These hub-control instructions take 2-9 clocks, except LOCKNEW which takes 4-11  |

## C-84: `cordic-fixed-latency-oversimplification` — 1 site · DeSilva

- **The defect:** 55 clocks is exact - Not 54, not 56. Always exactly 55 clocks from operation start to result ready.
- **Correct (true fact):** "When a cog issues a CORDIC instruction, it must wait for its hub slot, which is zero to (cogs-1) clocks away... Fifty-five clocks later, results will be available."
- **Source proof:** Silicon Doc v35 p2-documentation.txt:7290-7291

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | opus-master/COMPLETE-OPUS-MASTER.md:2512 (Ch | 55 clocks is exact - Not 54, not 56. Always exactly 55 clocks from operation sta → It is 55 clocks after the command is handed to the solver, but a cog must first  |

## C-85: `cordic-getq-stalls-not-undefined` — 1 site · Assembly (Part I)

- **The defect:** attempting to retrieve results before this period completes produces undefined values
- **Correct (true fact):** 'results will be available via the GETQX and GETQY instructions, which will wait for the results, in case they haven't arrived yet.' GETQX/GETQY stall until the result is ready (when an operation is in progress); they do not return undefined values. Undefined/empty return (QMT) happens only when NO operation is in progress.
- **Source proof:** Silicon Doc p2-documentation.txt lines 7290-7291, 7311; and this doc's own line 83

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.1.2 line 29 | attempting to retrieve results before this period completes produces undefined v → If GETQX/GETQY execute while the queued result is still computing, the cog stall |

## C-86: `cordic-latency-no-variation-overstated` — 1 site · DeSilva

- **The defect:** Every CORDIC result arrives in exactly 55 clock cycles with no variation
- **Correct (true fact):** The 54-stage pipeline delivers results 55 clocks after the command is handed off, but the cog first waits 0 to (cogs-1) clocks (0-7 on the 8-cog part) for its hub slot, and GETQX/GETQY themselves are 2...58 clocks. So the end-to-end time from issuing a CORDIC instruction is not perfectly invariant.
- **Source proof:** Silicon Doc v35 lines 7290-7291 ('it must wait for its hub slot, which is zero to (cogs-1) clocks away ... Fifty-five clocks later, results will be available')

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch7 What Just Happen | Every CORDIC result arrives in exactly 55 clock cycles with no variation → The CORDIC pipeline latency is a fixed 55 clocks, but the time from issuing the  |

## C-87: `cordic-overlap-example-overstated` — 1 site · DeSilva

- **The defect:** The sine-wave generation loop achieves perfect overlap of the 55-clock CORDIC latency with useful work
- **Correct (true fact):** The QROTATE result is not ready until 55 clocks after issue. The loop issues QROTATE and reads GETQY within the same iteration, only ~2-3 instructions (a handful of clocks) later, so GETQY stalls ~45+ clocks each pass. There is no cross-iteration pipelining, hence no 'perfect' overlap.
- **Source proof:** Silicon Doc v35 line 7291 (results available 55 clocks after handoff); loop body lines 2210-2217 issues QROTATE then reads GETQY ~3 instructions later

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch7 The CORDIC Pipel | The sine-wave generation loop achieves perfect overlap of the 55-clock CORDIC la → To actually overlap, software-pipeline across iterations: issue the next sample' |

## C-88: `cordic-overwrite-vs-pipeline-contradiction` — 1 site · DeSilva

- **The defect:** starting a new operation before retrieving your result overwrites it!
- **Correct (true fact):** "it is possible to overlap CORDIC commands, where several commands are initially given to the CORDIC solver, and then results are read... indefinitely"; results are only overwritten if interrupts steal clocks.
- **Source proof:** Silicon Doc v35 p2-documentation.txt:7293-7300

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | opus-master/COMPLETE-OPUS-MASTER.md:2510 (Ch | starting a new operation before retrieving your result overwrites it! → Multiple CORDIC operations can be in flight simultaneously; results queue and ar |

## C-89: `cordic-per-cog-fabrication` — 1 site · DeSilva

- **The defect:** Each cog has its own CORDIC, but starting a new operation before retrieving your result overwrites it!
- **Correct (true fact):** "In the hub, there is a 54-stage pipelined CORDIC solver that can compute the following functions for all cogs" — one shared solver in the hub, not one per cog.
- **Source proof:** Silicon Doc v35 p2-documentation.txt:7270-7271

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | opus-master/COMPLETE-OPUS-MASTER.md:2510 (Ch | Each cog has its own CORDIC, but starting a new operation before retrieving your → There is a single CORDIC solver in the hub, shared by all cogs (each cog gets a  |

## C-90: `cordic-pipeline-queue-overwrite` — 1 site · DeSilva

- **The defect:** Don't queue a new CORDIC op while one is pending - a second QMUL/QDIV/QFRAC before reading results overwrites the queue
- **Correct (true fact):** The CORDIC is a 54-stage pipeline. You may issue several commands before reading; results emerge in order and are read with GETQX/GETQY in sequence. Results are only lost if too many accumulate before reading, or if interrupts steal clocks during the juggle - not merely because a second op was issued.
- **Source proof:** Silicon Doc v35 lines 7293-7300 ('the pipeline is 54 clocks long, it is possible to overlap CORDIC commands, where several commands are initially given to the CORDIC solver, and then results are read and another command is given, indefinitely')

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch5 Common Gotchas i | Don't queue a new CORDIC op while one is pending - a second QMUL/QDIV/QFRAC befo → The CORDIC is pipelined - you may issue several operations before reading, and G |

## C-91: `cordic-qexp-base2-not-e` — 1 site · Assembly (Part I)

- **The defect:** Exponential \| QEXP \| e^x approximation in X
- **Correct (true fact):** QEXP: 'Begin CORDIC logarithm-to-number conversion of D. GETQX retrieves number.' Silicon: '- Compute 2 to the power of D'. QEXP is the base-2 exponential (5:27 log -> number), i.e. 2^x, NOT e^x.
- **Source proof:** v35 CSV row 249 (QEXP); Silicon Doc p2-documentation.txt lines 7432-7436

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.1.1 line 23 (CORDI | Exponential \| QEXP \| e^x approximation in X → QEXP computes 2^x (base-2 exponential of a 5:27 fixed-point value), the inverse  |

## C-92: `cordic-tangent-capability-overreach` — 1 site · DeSilva

- **The defect:** CORDIC can calculate sine, cosine, and tangent
- **Correct (true fact):** The hardware CORDIC functions are multiply, divide, square root, (X,Y) rotation, cartesian<->polar conversion, log, and exp. Sine and cosine come from QROTATE; tangent is not a native CORDIC output - it must be derived (sin/cos, i.e., a subsequent divide).
- **Source proof:** Silicon Doc v35 lines 7271-7285 (CORDIC function list: 32x32 multiply, 64/32 divide, sqrt, (X,Y) rotate, cartesian<->polar, log, exp)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch7 What Just Happen | CORDIC can calculate sine, cosine, and tangent → CORDIC directly yields sine and cosine (via QROTATE); tangent is not a native CO |

## C-93: `counter-ticks-elapsed-time-overstatement` — 1 site · IOSP

- **The defect:** Z reports the actual elapsed clocks — always ≥ X, never exactly X.
- **Correct (true fact):** For %10101 Z is the time ACCUMULATED WITHIN each measured period (equal to true elapsed only when periods are contiguous, i.e. single-pin rise-to-rise); and total is ≥ X but can equal X if a period boundary coincides with the X-th clock.
- **Source proof:** Silicon Doc part4-smart-pins.txt lines 761-800: '%10101 = For periods in X+ clock cycles, count time … accumulates time within each period'; 'until X clock cycles elapse and then any period in progress completes.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §15.3 P_COUNTER_TICKS note, line 170 | Z reports the actual elapsed clocks — always ≥ X, never exactly X. → Z is the accumulated in-period time (≈ elapsed clocks for a single-pin, back-to- |

## C-94: `counting-mode-reset-negative-adder-scope` — 1 site · IOSP

- **The defect:** Z = initial adder value: 0 or +1 for unidirectional counters; bidirectional modes (quadrature, up/down) can also load -1, accounting for any edge coincident with reset
- **Correct (true fact):** Only %01100 P_REG_UP resets to (0/1). The four other counting modes %01011 (quadrature), %01101 (up/down), %01110 (P_COUNT_RISES) AND %01111 (P_COUNT_HIGHS) all list the reset adder as (0/1/-1). So P_COUNT_RISES and P_COUNT_HIGHS can also load -1.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt: %01110 (P_COUNT_RISES) reset 'Z is set to the adder value (0/1/-1)'; %01111 (P_COUNT_HIGHS) 'Z is set to the adder value (0/1/-1)'; %01100 (P_REG_UP) '(0/1)' only

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-14-counting.md §1 | Z = initial adder value: 0 or +1 for unidirectional counters; bidirectional mode → The reset adder is 0 or +1 only for P_REG_UP; the other counting modes — quadrat |

## C-95: `creation-line-keyword-contradiction` — 1 site · Debug Window

- **The defect:** CARTESIAN, POLAR, and TEXTSIZE are runtime commands, not creation-line keywords — issue them after the window exists, not in the DEBUG(`PLOT ...) creation call
- **Correct (true fact):** The chapter's own worked examples put POLAR (line 145: `debug(`PLOT Rose SIZE 512 512 POLAR $1_0000 BACKCOLOR $000000)`) and TEXTSIZE (line 295: `debug(`PLOT Labels SIZE 600 400 BACKCOLOR $FFFFFF TEXTSIZE 14)`) directly on the creation line. v55's own TERM example likewise puts TEXTSIZE on a creation line.
- **Source proof:** ch05-plot.md line 145 (POLAR on creation line) and line 295 (TEXTSIZE on creation line); Spin2 v55 line 1299 shows TEXTSIZE on a TERM creation line

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch05-plot.md §Creating a PLOT window, line 5 | CARTESIAN, POLAR, and TEXTSIZE are runtime commands, not creation-line keywords  → CARTESIAN, POLAR, and TEXTSIZE are feeding commands (not window-instantiation ke |

## C-96: `crop-form-count-undercount` — 1 site · Debug Window

- **The defect:** CROP has three forms (Chapter 5 documents them in full), and each is one idiom of this technique.
- **Correct (true fact):** The v55 reference documents at least a fourth CROP form (CROP layer AUTO left_plot top_plot) beyond the three enumerated, and the v50 changelog also documents a two-coordinate 'CROP layer display_left display_top' form.
- **Source proof:** Spin2 v55 line 1286 (CROP with 0/4/6 coords) PLUS line 1287 'CROP layer AUTO left_plot top_plot'; v50 changelog also lists 'CROP layer_id display_left display_top' (2-coord form)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch15-panels.md §Technique 3, line 133 | CROP has three forms (Chapter 5 documents them in full), and each is one idiom o → CROP has more than three forms; this chapter uses three of them. Say 'CROP's thr |

## C-97: `ct-event-equals-vs-passes` — 1 site · DeSilva

- **The defect:** EVENT_CT1 %0001 CT equals CT1 (timer 1 target) [and CT2/CT3 rows]
- **Correct (true fact):** The CT event fires when CT reaches/passes the target (CT >= CT1) and the flag is sticky until cleared — it is not a momentary exact-equality condition.
- **Source proof:** Silicon Doc p2-documentation.txt lines 5298-5299: 'Set whenever CT passes the result of the ADDCT1 (MSB of CT minus CT1 is 0)'; line 5131: 'Event 1 = CT passed CT1'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | §'EVENT_* Constants' table, lines 5012-5014 | EVENT_CT1 %0001 CT equals CT1 (timer 1 target) [and CT2/CT3 rows] → EVENT_CT1: fires when CT reaches/passes the CT1 target. |

## C-98: `cycle-count-wrong` — 1 site · DeSilva

- **The defect:** 3-clock deterministic access via RDLUT / WRLUT
- **Correct (true fact):** RDLUT executes in 3 clocks; WRLUT executes in 2 clocks
- **Source proof:** v35 CSV row 151 (RDLUT): cog-clocks=3; row 220 (WRLUT): cog-clocks=2

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch13 'What We've Le | 3-clock deterministic access via RDLUT / WRLUT → LUT access is deterministic: RDLUT in 3 clocks, WRLUT in 2 clocks |

## C-99: `d-field-altd-hub-vs-cog-register` — 1 site · Assembly (Part I)

- **The defect:** The D field can also specify: Hub addresses (for ALTD-modified instructions)
- **Correct (true fact):** ALTD alters the next instruction's 9-bit D field to (D+S) & $1FF — a COG/LUT register address ($000-$1FF). Silicon Doc line 1013: 'Cog registers can be accessed indirectly most easily by using the ALTS/ALTD/ALTR instructions.' ALTD produces indirect cog-register addressing, never a hub address.
- **Source proof:** v35 CSV row 116 (ALTD D,{#}S): 'Alter D field of next instruction to (D + S) & $1FF'; Silicon Doc p2-documentation.txt line 1013

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.5.1 The  | The D field can also specify: Hub addresses (for ALTD-modified instructions) → The D field can also specify: indirect Cog/LUT register addresses (for ALTD-modi |

## C-100: `dac-reset-output-state-unsupported` — 1 site · IOSP

- **The defect:** During reset (DIR=0), for all DAC modes the Output = low (0V).
- **Correct (true fact):** For the DAC 16-bit dither modes the silicon states ONLY that IN is low and Y[15:0] is captured; it pointedly does NOT say the output is driven low (contrast the pulse/transition/NCO modes, where it explicitly does). With DIR=0 the pin driver is disabled, so the DAC output is not actively driven to 0V.
- **Source proof:** p2-documentation.txt lines 7925 & 7939 (DAC 16-bit dither modes): "During reset (DIR=0), IN is low and Y[15:0] is captured." — vs lines 7957/7965/7998 (pulse/transition/NCO): "During reset (DIR=0), IN is low, the output is low, ..."

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-10-dac-output.md §10.10 Quick Refere | During reset (DIR=0), for all DAC modes the Output = low (0V). → During reset (DIR=0): IN = low, Y[15:0] is captured (ready for DIR=1). The silic |

## C-101: `dat-label-immediate-address-not-value` — 1 site · IOSP

- **The defect:** The example configures smart pin 10: STEP_PIN is defined `STEP_PIN long 10` and then used as `#STEP_PIN` immediate in dirl/wrpin/wxpin/drvl/wypin/testp/rdpin.
- **Correct (true fact):** `#STEP_PIN` is an immediate whose value is the symbol's cog ADDRESS (13), not the datum stored there (10). To use the value 10 the operand must be the register `STEP_PIN` (no `#`), or STEP_PIN must be a CON. As written, dirl/wrpin/wxpin/drvl/wypin/testp/rdpin all act on pin 13, not pin 10.
- **Source proof:** pnut-ts 1.55.0 --list of the example: symbol STEP_PIN VALUE 00D00034 (cog address 0x0D = 13); DAT long holding value 10 sits at cog register 13.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §7.7 Example 4 (PASM2 Continuous Step Genera | The example configures smart pin 10: STEP_PIN is defined `STEP_PIN long 10` and  → Either declare `STEP_PIN = 10` in a CON block (so `#STEP_PIN` is immediate 10),  |

## C-102: `debug-cog-prefix-format` — 1 site · Assembly (Part I)

- **The defect:** DEBUG automatically prefixes each message with the cog number, written 'Cog0:' through 'Cog7:' (with a colon).
- **Correct (true fact):** 'DEBUG() messages always start with "CogN ", where N is the cog number, followed by two spaces' — the prefix is 'CogN' followed by spaces, with NO colon (report lines show 'Cog0 i = 0').
- **Source proof:** Spin2 v55 spin2-v55-text.txt line 908 (and example output line 1034 'Cog0 i = 0')

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.8.4 Multi-Cog Prog | DEBUG automatically prefixes each message with the cog number, written 'Cog0:' t → DEBUG prefixes each text message with 'CogN ' (the word Cog, the cog number, the |

## C-103: `default-value-editor-text-size` — 1 site · Debug Window

- **The defect:** TEXTSIZE default is 10.
- **Correct (true fact):** The SCOPE_XY TEXTSIZE default is the editor's text size (a user-configurable value inherited from the tool), not a fixed 10.
- **Source proof:** Spin2 v55 text line 1184: 'TEXTSIZE 6_to_200 \| Set the legend text size. \| editor text size'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch08-scope-xy.md §Creating a SCOPE_XY window | TEXTSIZE default is 10. → TEXTSIZE default is the editor text size (not a hard-coded 10); range 6-200. |

## C-104: `default-value-wrong` — 1 site · Debug Window

- **The defect:** POS default is 'cascaded'.
- **Correct (true fact):** The documented POS default is 0, 0.
- **Source proof:** Spin2 v55 text line 1178: 'POS left top \| Set the window position. \| 0, 0'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch08-scope-xy.md §Creating a SCOPE_XY window | POS default is 'cascaded'. → POS default is 0, 0 (per the Spin2 reference). |

## C-105: `dir-instruction-z-flag-not-changed` — 1 site · Assembly (Part I)

- **The defect:** DIRZ/DIRNZ Z-flag column shows '---' (Z not changed)
- **Correct (true fact):** With WCZ, both C AND Z receive the prior DIR bit: 'C,Z = DIR bit.' The Z flag IS affected (it takes the DIR bit value), so a Z effect of '---' (unchanged) is wrong.
- **Source proof:** v35 CSV row 353 (DIRZ) and row 354 (DIRNZ): flag effect 'C,Z = DIR bit.'; encoding EEEE 1101011 CZL

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.4.1 DIRZ | DIRZ/DIRNZ Z-flag column shows '---' (Z not changed) → The Z column should show the DIR bit (same as C), because DIRZ/DIRNZ with WCZ se |

## C-106: `dollar-current-address-scope` — 1 site · Assembly (Part I)

- **The defect:** $ means 'Current Cog address' only in PASM (ORG mode)
- **Correct (true fact):** $ evaluates to the current assembly address in whatever mode is active — a cog address under ORG, a hub address under ORGH — not exclusively ORG mode.
- **Source proof:** pnut-ts v1.55.0: `here long $` compiles inside an `orgh` DAT block (yields current hub address)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.10.3 Lab | $ means 'Current Cog address' only in PASM (ORG mode) → $ is the current assembly address in BOTH ORG (cog address) and ORGH (hub addres |

## C-107: `dollar-dollar-hub-address-fabrication` — 1 site · Assembly (Part I)

- **The defect:** $$ means 'Current Hub address' in PASM (ORGH mode)
- **Correct (true fact):** $$ is the DITTO block index variable (introduced v50) that iterates from 0 to count-1 inside a DITTO generative block; it is NOT a current-address token and is illegal outside a DITTO block. Current address (cog or hub) is given by $ in both ORG and ORGH modes (compiler-verified: single $ compiles in ORGH).
- **Source proof:** pnut-ts v1.55.0 error: '"$$" (DITTO index) is only allowed within a DITTO block, inside a DAT block'; Silicon/Spin2 v55 line 42 (DITTO, v50): '$$' iterates 0..count-1 within a DITTO generative block

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.10.3 Lab | $$ means 'Current Hub address' in PASM (ORGH mode) → Remove the $$ row. There is no '$$ = current hub address' token; $ gives the cur |

## C-108: `dotsize-pixels-vs-half-pixels` — 1 site · Debug Window

- **The defect:** DOTSIZE argument is in pixels and sets the dot diameter, range 2-20 (so DOTSIZE 6 = 6-pixel diameter dot).
- **Correct (true fact):** DOTSIZE units are HALF-pixels, not pixels; DOTSIZE 6 = a 3-pixel dot, and the 2..20 range is 1..10 pixels.
- **Source proof:** Spin2 v55 text line 1183: 'DOTSIZE 2_to_20 \| Set the dot size in half-pixels for showing sample points. \| 6'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch08-scope-xy.md §Creating a SCOPE_XY window | DOTSIZE argument is in pixels and sets the dot diameter, range 2-20 (so DOTSIZE  → DOTSIZE sets the dot size in half-pixels, 2-20 (default 6); a value of 6 draws a |

## C-109: `dual-encoder-a-input-misrouted` — 1 site · IOSP

- **The defect:** ' Velocity on pin 22 (periodic, same encoder signals) / WRPIN(VEL_PIN, P_QUADRATURE \| P_MINUS1_B)  where VEL_PIN=22
- **Correct (true fact):** A smart pin's A-input defaults to its own pin; P_PLUS1_B/P_MINUS1_B only redirect the B selector. VEL_PIN=22 therefore reads A from physical pin 22 and B from pin 21. The encoder A phase is on pin 20 (ENC_A=20 / POS_PIN=20), so the velocity pin never sees the encoder A signal.
- **Source proof:** part4-smart-pins.txt:546 / p2-documentation.txt:8052 — 'configure both A and B smart pins to quadrature mode, one continuous, one periodic'; %AAAA/%BBBB selectors (lines 13-36) redirect the B-input, not the A-input.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-14-counting.md §1 | ' Velocity on pin 22 (periodic, same encoder signals) / WRPIN(VEL_PIN, P_QUADRAT → To measure the same encoder on a second smart pin, its A-input must also be rout |

## C-110: `edge-vs-positive-edge-imprecision` — 1 site · IOSP

- **The defect:** Counts A-input edges. B-input controls direction: high=increment, low=decrement.
- **Correct (true fact):** Mode %01101 accumulates on A-input POSITIVE (rising) edges only, not on both edges; B level sets direction.
- **Source proof:** Silicon Doc part4-smart-pins.txt line 578-579 (%01101): 'Accumulate A-input positive edges with B-input supplying increment (B=1) or decrement (B=0)'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-f-mode-reference.md §Mode %01101 P_ | Counts A-input edges. B-input controls direction: high=increment, low=decrement. → Counts A-input positive (rising) edges. B-input controls direction: high=increme |

## C-111: `edio-fields-misattributed-to-smartpins` — 1 site · IOSP

- **The defect:** the muted fields (A/B input routing in bits [31:21] and the always-0 bit 0) belong to smart pin modes and are covered by the full field map in §4.2
- **Correct (true fact):** The AAAA/BBBB/FFF fields (D[31:21]) are input selectors + A,B logic and drive IN in non-smart-pin modes.
- **Source proof:** Silicon Doc part4-smart-pins.txt lines 13-50 (WRPIN D operand: %AAAA_BBBB_FFF_... = A/B input selectors + A,B logic) and line 50: 'The resultant A will drive the IN signal in non-smart-pin modes.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-1-fundamentals/chapter-02-enhanced-dire | the muted fields (A/B input routing in bits [31:21] and the always-0 bit 0) belo → The A/B input-routing fields in bits [31:21] are low-level pin-config fields use |

## C-112: `event-branch-naming` — 1 site · Assembly (Part I)

- **The defect:** branched on (JSE/JNSE)
- **Correct (true fact):** There are no generic instructions named JSE or JNSE; the branch-on-selectable-event instructions are per-event: JSE1/JSE2/JSE3/JSE4 and JNSE1/JNSE2/JNSE3/JNSE4.
- **Source proof:** CSV rows 185-188 (JSE1..JSE4), 201-204 (JNSE1..JNSE4); Silicon Doc 5439 ('The matched JSEn and JNSEn branch instructions')

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.5.3 Pin-Based Synchr | branched on (JSE/JNSE) → branched on (JSEn/JNSEn, n = 1..4) |

## C-113: `event-constants-waitse-misapplication` — 1 site · DeSilva

- **The defect:** You can also use these constants with WAITSE/POLLSE by first triggering them with the appropriate hardware condition, then waiting.
- **Correct (true fact):** WAITSE1..4 and POLLSE1..4 are fixed per-channel instructions that take no event-number operand; the EVENT_* selector constants are consumed by SETINT1/2/3 (D[3:0]) only.
- **Source proof:** v35 CSV rows 275/291 (POLLSE1/WAITSE1): dedicated per-channel opcodes with no operand; SETINT1 row 310: 'Set INT1 source to D[3:0]'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | §'Using EVENT_* with SETINT' Pro tip, line 5 | You can also use these constants with WAITSE/POLLSE by first triggering them wit → The EVENT_* constants are used only with SETINT1/2/3. WAITSE/POLLSE are dedicate |

## C-114: `event-int-setint-off-semantics` — 1 site · DeSilva

- **The defect:** The SETINT1/2/3 instructions select which event triggers an interrupt using these constants: EVENT_INT %0000 = An interrupt occurred (INT1/2/3 fired)
- **Correct (true fact):** For SETINT1/2/3 (interrupt-source selection, D[3:0]), source value 0 is <off> and DISABLES the interrupt. The 'interrupt-occurred' meaning of EVENT_INT applies to POLL/WAIT usage, not SETINT.
- **Source proof:** Silicon Doc p2-documentation.txt line 5502: '0 = <off>, default on cog start for INT1/INT2/INT3 event sources'; Spin2 v55 spin2-v55-text.txt line 1641: 'EVENT_INT / INT_OFF \| Interrupt-occurred event or interrupts off'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | §'EVENT_* Constants: When You Need Interrupt | The SETINT1/2/3 instructions select which event triggers an interrupt using thes → EVENT_INT (0) is the interrupt-occurred event for POLL/WAIT; when passed to SETI |

## C-115: `event-mode-rises-vs-high` — 1 site · IOSP

- **The defect:** Comment labels SETSE1 mode %001 as 'Event on IN high'.
- **Correct (true fact):** SETSE1 mode %001 triggers on a RISING EDGE of IN, not on IN being high; the level-high event is mode %11x.
- **Source proof:** p2-documentation.txt L5471 '%001_PPPPPP = INA/INB bit of pin %PPPPPP rises'; L5474 '%11x_PPPPPP = ... is high'. YAML deliverables/ai/P2/language/pasm2/setse1.yaml confirms '%001 = rises (positive edge)', '%11x = is high (level detection)'.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-16-adc.md §16.7 Example 5, line 559 | Comment labels SETSE1 mode %001 as 'Event on IN high'. → Comment should read 'Event on IN rising edge' (mode %001); an IN-high level even |

## C-116: `external-psram-labeled-onchip-resource` — 1 site · Architect's Guide

- **The defect:** the agent helps decide how to reach it with the P2's own resources — LUT RAM, PSRAM, the CORDIC, the streamer
- **Correct (true fact):** The P2's on-chip resources are cogs, hub RAM (512 KB), smart pins, the CORDIC solver, the streamer, LUT RAM, and 16 locks. PSRAM/HyperRAM is external memory a P2 design interfaces to via pins/streamer — it is not a P2 on-chip resource and is not part of the silicon at all.
- **Source proof:** Silicon Doc v35 p2-documentation.txt L234 ('P2X8C4M64P contains 8 cogs, 512 KB of hub RAM, and 64 smart I/O pins') + full-doc grep for 'psram/hyperram' returns ZERO hits

| Document | Location | before → after |
|----------|----------|----------------|
| Architect's Guide | architect-guide-body.md Ch.12 'Building and  | the agent helps decide how to reach it with the P2's own resources — LUT RAM, PS → List only genuine on-chip resources as the P2's own (LUT RAM, the CORDIC, the st |

## C-117: `false-negative-capability-denial` — 1 site · P2AN005

- **The defect:** which would need a hardware mutex the P2 doesn't have
- **Correct (true fact):** The P2 has a hub lock pool of hardware locks (semaphores) that grant one cog at a time exclusive 'owner' status across cogs — i.e. hardware mutexes. LOCKTRY takes a lock, LOCKREL releases it, and while held no other cog can take it.
- **Source proof:** Silicon Doc v35 p2-documentation.txt LOCKS section (~lines 7455-7490): 'locks are just a means of allowing one cog at a time the exclusive status of "owner"'; LOCKNEW/LOCKTRY/LOCKREL/LOCKRET instructions allocate/take/release from the hub lock pool.

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN005 | P2AN005.md §Adapt It / Going Further, line 3 | which would need a hardware mutex the P2 doesn't have → The P2 DOES provide hardware mutual-exclusion primitives — 16 hub locks (LOCKNEW |

## C-118: `fft-legend-field-mislabel` — 1 site · Debug Window

- **The defect:** grid — Grid flags: bit 0 = baseline line, bit 1 = top line.
- **Correct (true fact):** The 6th channel argument is the 'legend' field, a 4-bit %abcd value: bit3=max legend text, bit2=min legend text, bit1=max line, bit0=min line.
- **Source proof:** Spin2 v55 line 1219: legend field is '%abcd, where %a to %d enable max legend, min legend, max line, min line.'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch09-fft.md §Feeding samples (channel-arg ta | grid — Grid flags: bit 0 = baseline line, bit 1 = top line. → This is the 'legend' field (%abcd): bit0=min/baseline line, bit1=max/top line, b |

## C-119: `fft-negative-linesize-semantics` — 1 site · Debug Window

- **The defect:** LINESIZE: Line width (−32–32; negative draws filled bars).
- **Correct (true fact):** A negative LINESIZE makes isolated vertical lines (stem/impulse style); units are half-pixels; default 3.
- **Source proof:** Spin2 v55 line 1212: 'LINESIZE neg32_to_32 \| Set the line size in half-pixels ... A negative line size will make isolated vertical lines. \| 3'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch09-fft.md §Creating (config table) line 81 | LINESIZE: Line width (−32–32; negative draws filled bars). → Negative LINESIZE draws isolated vertical lines (not connected), not 'filled bar |

## C-120: `fft-textsize-default-invented-number` — 1 site · Debug Window

- **The defect:** TEXTSIZE default is 'font (≈11)'.
- **Correct (true fact):** The TEXTSIZE default is the editor text size (whatever the user's editor is configured to), not a fixed ~11.
- **Source proof:** Spin2 v55 line 1213: 'TEXTSIZE 6_to_200 \| Set the legend text size. \| editor text size'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch09-fft.md §Creating (config table) line 82 | TEXTSIZE default is 'font (≈11)'. → Default TEXTSIZE is the editor's text size; do not pin it to ≈11. |

## C-121: `field-range-scope-error` — 1 site · IOSP

- **The defect:** X[3:0]: Sample period exponent (1-15)
- **Correct (true fact):** WXPIN sets sample period to POWER(2, X[3:0]); X[3:0] is a 4-bit field with valid values %0000 (1 clock) through %1111 (32768 clocks). For SINC2 Sampling mode (%00), %1110 and %1111 are marked 'overflow', so the useful exponent range is 1-13, not 1-15; and value 0 (1 clock) is a legal field value (used by bitstream-capture mode).
- **Source proof:** silicon-doc part4-smart-pins.txt:816 + period table lines 826-856

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | Appendix C, ADC Sample Rate section, Variabl | X[3:0]: Sample period exponent (1-15) → X[3:0] is a 4-bit sample-period exponent (field range 0-15, period = 2^X[3:0] cl |

## C-122: `fifo-wrap-address-alignment-wrong` — 1 site · Streamer

- **The defect:** Buffer address aligned to 64-byte boundary for wrap mode
- **Correct (true fact):** For wrapping, the hub START ADDRESS must be long-aligned (address ends in %00, i.e. 4-byte / long alignment) 'since there won't be an extra cycle in which to read/write a portion of a long'. The 64-byte unit is the granularity of the BLOCK COUNT (D operand), not a requirement on the buffer address.
- **Source proof:** Silicon Doc v35 p2-documentation.txt line 6673 + RDFAST/WRFAST/FBLOCK encoding line 6702: S/# = 'start address for wrapping (long-aligned)', bits end in AA00

| Document | Location | before → after |
|----------|----------|----------------|
| Streamer | Appendix D §"Corrupted Data from RDFAST", ch | Buffer address aligned to 64-byte boundary for wrap mode → For wrap mode the buffer START ADDRESS must be long-aligned (4-byte, address end |

## C-123: `filter-length-mismatch` — 1 site · P2AN004

- **The defect:** If a turned knob jumps or counts backward, add `P_FILT1_AB` to the mode for two-clock input filtering
- **Correct (true fact):** P_FILT1_AB selects the global FILT1 setting, whose reset default is length 1 (3 flipflops), tap 5, ~600 ns low-pass time. The ~2-clock (12.5 ns, 2-flipflop, tap-0) profile is the reset default of FILT0 (P_FILT0_AB), not FILT1.
- **Source proof:** Silicon Doc part3-pages-37-38.txt lines 25,52-58: filter length 2/3/5/8 flipflops selected by 0..3; reset defaults filt0=len0(2ff)/tap0/12.5ns, filt1=len1(3ff)/tap5/600ns. spin2-v55 line 1451: P_FILT1_AB selects FILT1 settings.

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN004 | P2AN004.md §Recipe R3, Hardware callout, lin | If a turned knob jumps or counts backward, add `P_FILT1_AB` to the mode for two- → add `P_FILT1_AB` to select the global FILT1 filter setting (reset default: 3-fli |

## C-124: `fractional-baud-condition-omitted` — 1 site · IOSP

- **The defect:** X[15:10] provides fractional (1/64-clock) baud precision (presented unconditionally, and tabulated for 9600-115200 baud)
- **Correct (true fact):** The fractional field X[15:10] is honored by hardware ONLY when X[31:26] is zero, i.e. when the integer bit period < 1024 clocks. Above that the fractional bits are ignored.
- **Source proof:** Silicon Doc p2-documentation.txt line ~9089 (%11110): 'X[31:16] establishes the number of clocks in a bit period, and in case X[31:26] is zero, X[15:10] establishes the number of fractional clocks in a bit period.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | X[15:10] provides fractional (1/64-clock) baud precision (presented unconditiona → State that X[15:10] fractional clocks apply only when X[31:26]=0 (integer bit pe |

## C-125: `fractional-baud-ignored-when-period-large` — 1 site · IOSP

- **The defect:** Using X[15:10] fractional timing gives <0.001% error at 115200 baud
- **Correct (true fact):** The fractional field X[15:10] is honored ONLY when X[31:26]==0 (integer bit period < 1024 clocks). At 115200 baud @200MHz the period is 1736 clocks, so the hardware ignores the fractional bits; the achievable error equals the integer-only error (~0.006%), not <0.001%.
- **Source proof:** Silicon-doc p2-documentation.txt async-serial-transmit: 'X[31:16] establishes the number of clocks in a bit period, and IN CASE X[31:26] IS ZERO, X[15:10] establishes the number of fractional clocks.' At 200MHz/115200 baud bit period = 1736 clocks; X[31:16]=1736 (>=1024) so X[31:26] != 0 → fractiona

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | Using X[15:10] fractional timing gives <0.001% error at 115200 baud → Fractional timing improves accuracy ONLY when the integer bit period is < 1024 c |

## C-126: `fractional-baud-missing-caveat` — 1 site · IOSP

- **The defect:** Fractional \| X[15:10] \| 1/64 clock precision
- **Correct (true fact):** The field location (X[15:10]) and 1/64 precision are correct, but the entry omits the load-bearing constraint that fractional bits are honored ONLY when X[31:26]==0 (integer period < 1024 clocks) — otherwise ignored. Presented unqualified next to 115200@200MHz examples, this misleads.
- **Source proof:** Silicon-doc p2-documentation.txt async-serial-transmit: fractional X[15:10] applies 'in case X[31:26] is zero' only.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | Fractional \| X[15:10] \| 1/64 clock precision → Fractional \| X[15:10] \| 1/64 clock precision — honored only when the integer b |

## C-127: `fractional-comment-vs-integer-code` — 1 site · IOSP

- **The defect:** bit_period := (_clkfreq / BAUD) << 16 calculates the bit period with fractional precision
- **Correct (true fact):** Fractional precision requires multiplying the FULL (non-truncated) clocks-per-bit by 65536 then masking; (_clkfreq / BAUD) truncates to integer BEFORE the <<16, discarding the fraction (X[15:10]=0).
- **Source proof:** Doc §11.2 lines 59-61 (its own fractional formula): bit_period = (sysclk / baud_rate) × 65536; X[31:10] = bit_period & $FFFFFC00. Silicon line ~9090: '(clocks * $1_0000) & $FFFFFC00'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | bit_period := (_clkfreq / BAUD) << 16 calculates the bit period with fractional  → Comment should read 'integer bit period' — or the code should be bit_period := ( |

## C-128: `frequency-counter-exactness-overstatement` — 1 site · IOSP

- **The defect:** For a 1-second window, period_count = frequency in Hz (direct equality).
- **Correct (true fact):** X is the MINIMUM window; the actual window extends past X to complete the final period, so period_count is complete periods over slightly-more-than-1-second, not an exact Hz reading (also ±1 period quantization per the doc's own §15.7).
- **Source proof:** Silicon Doc part4-smart-pins.txt line 763 '%10111 = For periods in X+ clock cycles' + line ~785 'until X clock cycles elapse and then any period in progress completes'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §15.3 P_COUNTER_PERIODS frequency calc, line | For a 1-second window, period_count = frequency in Hz (direct equality). → For a ~1-second window, period_count ≈ frequency in Hz (approximate — the window |

## C-129: `frequency-counter-mode-recommendation-inconsistency` — 1 site · IOSP

- **The defect:** The worked example titled 'Frequency Counter' (Example 1) implements the frequency counter with P_COUNT_RISES.
- **Correct (true fact):** Both modes count A-input positive edges over an X-clock window, so either produces a valid frequency count; the mismatch is internal editorial inconsistency, not a silicon error.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt: both %01100 (P_REG_UP, count A when B high) and %01110 (P_COUNT_RISES, count A edges) can count edges over a period — both technically valid for a gated frequency count

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-14-counting.md §1 | The worked example titled 'Frequency Counter' (Example 1) implements the frequen → Make the mode-selection guidance and the worked example agree — either recommend |

## C-130: `frequency-counter-resolution-error` — 1 site · IOSP

- **The defect:** For a period-counting frequency measurement, a 10 ms gate gives 10 Hz (1%) resolution at 1 kHz and 10 kHz (1%) at 1 MHz; 100 ms gives 1 Hz/1 kHz (0.1%); 1 s gives 0.1 Hz/100 Hz (0.01%).
- **Correct (true fact):** A direct period counter's absolute resolution is 1/gate_time, INDEPENDENT of signal frequency: 10 ms→100 Hz, 100 ms→10 Hz, 1 s→1 Hz. The RELATIVE resolution is 1/(f·gate) and therefore CANNOT be the same at 1 kHz and 1 MHz — it differs by 1000×.
- **Source proof:** Direct-period-counter quantization physics (f_meas = N/gate, N is integer ±1) + this doc's own §15.7 line 508 "P_COUNTER_PERIODS ... 1 period ... ±1 period per window"

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §15.7 Gate Time vs Resolution table, line 52 | For a period-counting frequency measurement, a 10 ms gate gives 10 Hz (1%) resol → At a 10 ms gate the resolution is ~100 Hz regardless of frequency (≈10% at 1 kHz |

## C-131: `getct-64bit-latch-mechanism` — 1 site · DeSilva

- **The defect:** To capture the full 64-bit count you must read upper (GETCT D WC), lower (GETCT D), then upper again, and retry if the upper word changed.
- **Correct (true fact):** GETCT WC latches the full 64-bit counter and returns the upper 32 bits; the immediately-following plain GETCT returns the latched lower 32 bits of that same instant (which is why the WC+plain pair must not be interrupt-separated). The pair is atomic — there is no tear to retry against.
- **Source proof:** CSV row 260 (GETCT): 'GETCT WC + GETCT gets full CT'; Silicon Doc line 5674 lists GETCT+WC among ops that must not be interrupt-separated; line 81 'GETCT WC retrieves upper 32-bits'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.12 'Pitfall — CT  | To capture the full 64-bit count you must read upper (GETCT D WC), lower (GETCT  → Use the atomic idiom: 'GETCT hi WC' immediately followed by 'GETCT lo' — GETCT W |

## C-132: `getct-double-overhead` — 1 site · Assembly (Part I)

- **The defect:** This measurement includes the cycles consumed by GETCT itself (2 cycles each) ... Measuring a 10-cycle sequence with two GETCT instructions reports 14 cycles (2 + 10 + 2)
- **Correct (true fact):** GETCT is a 2-clock instruction reading the free-running counter. Two GETCTs separated by a 10-cycle payload sample CT exactly 12 clocks apart (2 for the first GETCT + 10 payload), so the difference is 12. Only ONE GETCT's execution falls inside the measured interval; the second GETCT samples at its start, after the interval.
- **Source proof:** CSV row 260 GETCT (2 clocks, 'CT++ on every clock'); back-to-back GETCT difference = 2

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.7.1 The Cycle Counte | This measurement includes the cycles consumed by GETCT itself (2 cycles each) .. → Two GETCTs bracketing a 10-cycle sequence report 12 cycles (2 overhead + 10), no |

## C-133: `getscp-missing-setscp` — 1 site · IOSP

- **The defect:** getscp combined  ' Read all 4 channels (32-bit)
- **Correct (true fact):** 'The SETSCP instruction enables the SCOPE data pipe and selects the 4-pin block' that GETSCP then reads. GETSCP returns valid four-channel data only after SETSCP has enabled the pipe and selected the block.
- **Source proof:** Silicon Doc v35, p2-documentation.txt lines 8816-8835

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §16.5 Reading Scope Data, line 363 | getscp combined  ' Read all 4 channels (32-bit) → Enable and point the SCOPE data pipe first with SETSCP (D[6]=1, D[5:2]=4-pin blo |

## C-134: `glob-overgeneralization` — 1 site · Assembly (Part I)

- **The defect:** The TEST* instructions (TESTP, TESTPN, TESTB, TESTBN) ... reject WCZ.
- **Correct (true fact):** The glob 'TEST*' also matches TEST and TESTN, which BOTH carry full WC/WZ/WCZ. Only the pin/bit-test forms (TESTP/TESTPN/TESTB/TESTBN) reject WCZ.
- **Source proof:** v35 CSV rows 81 TEST 'D,{#}S {WC/WZ/WCZ}' and 83 TESTN '{WC/WZ/WCZ}'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.2.6 line 180 | The TEST* instructions (TESTP, TESTPN, TESTB, TESTBN) ... reject WCZ. → Avoid the 'TEST*' family label here; say 'the bit/pin test instructions TESTP, T |

## C-135: `hub-access-2plus-wait-oversimplification` — 1 site · Assembly (Part I)

- **The defect:** Hub access \| 2 + hub wait \| 2 + hub wait
- **Correct (true fact):** A standalone RDLONG is 9...16 clocks in cog mode and 9...26 in hub-exec mode. The '2 base + wait' model yields 2...9, which is 7 clocks too low.
- **Source proof:** CSV RDLONG cog 9...16, hub-exec 9...26; Silicon Doc INSTRUCTION-TIMING

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.8.3 Timing Compariso | Hub access \| 2 + hub wait \| 2 + hub wait → Hub access \| 9...16 clocks \| 9...26 clocks (data-access timing is essentially  |

## C-136: `hub-access-latency-off-by-one` — 1 site · DeSilva

- **The defect:** you wait at most 8 clocks (P2) for hub access
- **Correct (true fact):** With 8 cogs the worst-case wait to reach the desired hub slice is up to #cogs-1 = 7 clocks, not 8.
- **Source proof:** Silicon Doc v35 line 6641: 'When a cog wants to read or write the hub RAM, it must wait up to #cogs-1 clocks to access the initial RAM slice of interest.'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Ch2 §The Egg Beater Revolution, line 596 | you wait at most 8 clocks (P2) for hub access → you wait at most 7 clocks (#cogs-1) to reach your hub slice, and often less if y |

## C-137: `hub-address-missing-augs` — 1 site · DeSilva

- **The defect:** To load the hub address of a DAT label into a register in PASM you write `mov ptr, @hub_data` (plain `@`, no augment).
- **Correct (true fact):** Hub addresses are byte-oriented and DAT labels typically live well above $1FF; a plain `#`/`@` immediate carries only 9 bits, so a full 32-bit hub address requires the `##` (AUGS) augment.
- **Source proof:** Silicon Doc p2-documentation.txt line ~6474 (HUB RAM: hub addresses byte-oriented); CSV MOV encoding has a 9-bit S immediate (##/AUGS required for values >511)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Reference Operators | To load the hub address of a DAT label into a register in PASM you write `mov pt → Use `mov ptr, ##@hub_data` — a DAT label's hub address usually exceeds the 9-bit |

## C-138: `hub-alignment-timing-fabrication` — 1 site · DeSilva

- **The defect:** Non-long-aligned hub access is slower and long-aligned access is faster/predictable ($1001 slower, $1000 faster)
- **Correct (true fact):** 'There are no special alignment rules for words and longs in hub RAM. Cogs can read and write bytes, words, and longs at any hub address.' RDLONG timing (9...16) is the same regardless of long-alignment.
- **Source proof:** Silicon Doc v35 p2-documentation.txt line 6474 (HUB RAM)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Chapter 12 §Hub Access Optimization, COMPLET | Non-long-aligned hub access is slower and long-aligned access is faster/predicta → P2 hub RAM has no alignment penalty — an RDLONG from $1001 costs the same 9-16 c |

## C-139: `hub-burst-mechanism` — 1 site · Assembly (Part I)

- **The defect:** Once a cog has started transferring during its hub window, it can continue occupying subsequent windows; the hub controller grants consecutive windows to a cog performing a burst.
- **Correct (true fact):** The cog does not occupy successive round-robin windows; the egg-beater maps sequential addresses to sequential RAM slices, so after the initial slot-wait the cog reads one long per clock from the next slice each cycle — other cogs still access their own slices concurrently.
- **Source proof:** Silicon Doc v35 lines 6634-6642 (Egg-Beater slices)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.3.3 Hub Burst Transf | Once a cog has started transferring during its hub window, it can continue occup → Bursts are fast because the egg-beater presents the next sequential long from th |

## C-140: `hub-exec-pc-range-extent` — 1 site · Assembly (Part I)

- **The defect:** Execution-modes table lists the Hub Execution PC Range as '$00400-$7FFFF'.
- **Correct (true fact):** Hub execution mode is defined by PC in $00400-$FFFFF (any PC >= $400), not $00400-$7FFFF. The doc equates the hub-exec PC range with the 512KB RAM extent ($7FFFF).
- **Source proof:** Silicon Doc p2-documentation.txt line 741: 'When the PC is in the range of $00400 and $FFFFF, the cog is fetching instructions from hub RAM. This is commonly referred to as hub execution mode.'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-01-execution-model.md §1.6 table lin | Execution-modes table lists the Hub Execution PC Range as '$00400-$7FFFF'. → Hub execution occurs for any PC at or above $00400 (silicon range $00400-$FFFFF) |

## C-141: `hub-immediate-bit-width` — 1 site · DeSilva

- **The defect:** A bare #address only encodes 9 bits ... Always use ## for hub addresses outside the 0–511 range.
- **Correct (true fact):** For RDBYTE/RDWORD/RDLONG/WRxxx a bare '#' hub address is only an 8-bit immediate (0-255). The 9-bit S field's top bit selects PTR-expression mode, so values 256-511 are NOT addresses; the compiler rejects `#300` as a hub address.
- **Source proof:** Silicon Doc v35 p2-documentation.txt L6913-6925 (hub address forms: '#$00..$FF - 8-bit immediate hub address'; '#%0AAAAAAAA - No AUGS, 8-bit immediate address' vs '#%1SUPNNNNN - PTR expression'); pnut-ts 1.55.0: `rdlong x,#300` -> ERROR 'Constant must be from 0 to 255'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md, Ch.4 Common Gotchas | A bare #address only encodes 9 bits ... Always use ## for hub addresses outside  → A bare `#` hub address only encodes 8 bits (0-255) on RDxxx/WRxxx; use `##` for  |

## C-142: `hub-op-constant-timing` — 1 site · Assembly (Part I)

- **The defect:** wrlong ##dest, ##addr takes 6 cycles (AUGD+AUGS+instr)
- **Correct (true fact):** WRLONG is a hub-memory write with VARIABLE timing (cog mode 3...10 clocks, not a fixed 2). It can never demonstrate constant timing.
- **Source proof:** CSV row 223 WRLONG: cog clocks '3...10*' (hub-exec variants 3...20/3...18/3...38)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-02-instruction-format.md §2.7.3 Timi | wrlong ##dest, ##addr takes 6 cycles (AUGD+AUGS+instr) → AUGD + AUGS add +4 clocks; WRLONG itself is variable (3...10 cog clocks), so the |

## C-143: `hub-op-cycle-undercount` — 1 site · Assembly (Part I)

- **The defect:** wrlong ##data, ##addr ' 6+ cycles (2+2+2: AUGD+AUGS+instr)
- **Correct (true fact):** WRLONG cog execution is 3...10 clocks (variable hub write), never 2; AUGD=2, AUGS=2. Minimum total = 2+2+3 = 7 clocks, ranging up to 14 — no hub op executes in 2 clocks.
- **Source proof:** v35 CSV row 223 (WRLONG {#}D,{#}S/P): cog clocks '3...10 *'; rows 408/409 (AUGS/AUGD #n): '2' each

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-06-address-modes.md §6.3.4 Augmentat | wrlong ##data, ##addr ' 6+ cycles (2+2+2: AUGD+AUGS+instr) → wrlong ##data, ##addr takes at least 7 clocks and is variable: AUGD (2) + AUGS ( |

## C-144: `hub-sequential-throughput-overclaim` — 1 site · DeSilva

- **The defect:** Sequential plain RDLONG with ptra++ gives 'Optimal hub slot usage' / 'Maximum throughput' — hardware manages the sequence
- **Correct (true fact):** Plain RDLONG is 9...16 clocks each with no pipelining; ptra++ only auto-increments the pointer. Maximum sequential throughput requires the FIFO (RDFAST/RFLONG) or a SETQ block transfer, not plain sequential RDLONG.
- **Source proof:** v35 CSV row 154 RDLONG 9...16; row 226 RDFAST / row 252 RFLONG (FIFO) 2 clocks

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Chapter 12 §Hub Access Optimization, COMPLET | Sequential plain RDLONG with ptra++ gives 'Optimal hub slot usage' / 'Maximum th → Sequential RDLONG ptra++ is convenient but each read still costs 9-16 clocks; tr |

## C-145: `hub-unaligned-masking-fabrication` — 1 site · DeSilva

- **The defect:** RDLONG and WRLONG work on long boundaries. If your address isn't a multiple of 4, the P2 silently masks the low bits.
- **Correct (true fact):** P2 random-access RDLONG/WRLONG support UNALIGNED hub addresses (any byte address); crossing a slice boundary just costs one extra clock. Only the FIFO WRAPPING mode requires long-alignment. There is no documented low-bit masking on random RDLONG/WRLONG.
- **Source proof:** Silicon Doc v35 p2-documentation.txt L6673 (FIFO wrapping): 'your hub start address must be long-aligned ... since there won't be an extra cycle in which to read/write a portion of a long in an extra hub RAM slice'; RDLONG CSV row 154 timing '9...16' (variable, includes the extra-slice cost)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md, Ch.4 Common Gotchas | RDLONG and WRLONG work on long boundaries. If your address isn't a multiple of 4 → RDLONG/WRLONG can read or write a long starting at ANY byte address; an unaligne |

## C-146: `hub-variable-timing-fabrication` — 1 site · Assembly (Part I)

- **The defect:** The conditional version maintains constant 3-cycle timing.
- **Correct (true fact):** The conditional version contains if_nz RDLONG; when the ready bit is set RDLONG executes as a variable-latency hub op, so timing is neither constant nor 3 cycles.
- **Source proof:** v35 CSV: RDLONG cog-clocks '9...16' / hub '9...26' — variable hub op

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.3.2 line 233 | The conditional version maintains constant 3-cycle timing. → Timing is not constant: when ready, RDLONG adds 9-26 variable clocks; the sequen |

## C-147: `hubexec-fetch-latency-mischaracterization` — 1 site · Assembly (Part I)

- **The defect:** Hub execution mode adds instruction fetch latency
- **Correct (true fact):** In hub-exec mode the prefetch FIFO streams sequential instructions ahead of execution, so straight-line code runs at 2 cycles/instruction with no per-instruction fetch latency. The added cost falls only on taken branches (FIFO refill, min 13 clocks).
- **Source proof:** Silicon Doc v35 (FIFO instruction streaming); CSV JMP hub-exec 13...20 vs cog 4

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.8 Key Concepts box,  | Hub execution mode adds instruction fetch latency → Hub execution mode adds a branch-refill penalty (a taken branch costs a minimum  |

## C-148: `immediate-vs-contents` — 1 site · DeSilva

- **The defect:** To point PTRA at the buffer whose hub address Spin2 stored in `buffer_addr` (a `long 0` 'Set by Spin2 at startup'), use `mov ptra, ##buffer_addr`.
- **Correct (true fact):** `##symbol` is the compile-time address of the symbol; to read the runtime hub pointer that Spin2 wrote into the register you must read the register contents: `mov ptra, buffer_addr`.
- **Source proof:** pnut_ts / MOV semantics: `##buffer_addr` loads the symbol's own (cog) address as a 32-bit immediate, not the value stored in that register

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §A Complete Example, | To point PTRA at the buffer whose hub address Spin2 stored in `buffer_addr` (a ` → `mov ptra, buffer_addr` — read the register contents (the hub pointer Spin2 stor |

## C-149: `in-flag-mechanism-misattribution` — 1 site · IOSP

- **The defect:** IN flag not acknowledged -> Accumulator overflow (as the reason a mode stops producing IN flags)
- **Correct (true fact):** When IN is left un-acknowledged it stays high and cannot be re-raised on the next event, so the cog stops seeing new IN flags. The cause is the missing acknowledge that keeps IN latched high — not accumulator overflow.
- **Source proof:** Silicon Doc part4-smart-pins.txt L150-155: acknowledge (WRPIN/WXPIN/WYPIN/RDPIN/AKPIN) 'causes the smart pin to lower its IN signal so that it can be raised again on the next event'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-e-troubleshooting.md §"Mode Stops W | IN flag not acknowledged -> Accumulator overflow (as the reason a mode stops pro → IN flag not acknowledged - IN stays high and cannot be re-raised for the next ev |

## C-150: `in-flag-repository-vs-sample-period` — 1 site · IOSP

- **The defect:** **All modes**: IN raised when sample period completes
- **Correct (true fact):** In long-repository mode (non-DAC) IN is raised whenever WXPIN updates the long ('When active (DIR=1), WXPIN updates the long and raises IN') — there is NO sample period. Only the three DAC modes tie IN to sample-period completion.
- **Source proof:** Silicon Doc part4-smart-pins.txt line 227 (repository) vs lines 241/265/297 (DAC modes)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-18-repository.md §18.8 Key Points, l | **All modes**: IN raised when sample period completes → Split the bullet: 'DAC modes: IN raised at sample-period completion; Repository: |

## C-151: `in-flag-semantics-completion-vs-buffer` — 1 site · IOSP

- **The defect:** repeat until PINREAD(MOSI_PIN)   ' Wait for completion
- **Correct (true fact):** For P_SYNC_TX, IN signals buffer-ready (word advanced into shifter), not clocking-complete. In start-stop mode the single WYPIN'd word flows through to the shifter and raises IN independent of the external P_TRANSITION clock finishing, so PINREAD can pass before the 8 clocks complete. Sync-serial TX has no IN 'transmission complete' semantic (unlike async, which exposes a busy flag via RDPIN WC).
- **Source proof:** Silicon-doc p2-documentation.txt sync-serial-transmit (%11100): 'Upon shifting each word, the buffered data written via WYPIN is advanced into the shifter and IN is raised, indicating that a new output word can be buffered'; start-stop: WYPIN before first clock 'flowing right through the buffer into

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | repeat until PINREAD(MOSI_PIN)   ' Wait for completion → IN on a sync-serial-TX pin means 'buffer empty / ready for next word', not 'tran |

## C-152: `incomplete-set-presented-as-exhaustive` — 1 site · Debug Window

- **The defect:** The value-only output formatters are `UDEC_`, `SDEC_`, `UHEX_`, `SHEX_`, and `UBIN_`
- **Correct (true fact):** The value-only (`_`-suffixed) convention applies to ALL DEBUG output commands, so the family is far larger than five (also SBIN_, FDEC_, ZSTR_, LSTR_, and every _BYTE/_WORD/_LONG/_ARRAY variant).
- **Source proof:** Spin2 v55 line 918: 'All DEBUG() output commands have alternate versions, ending in "_" which output only the value'; lines 948-953 show UDEC_BYTE/WORD/LONG/_ARRAY families

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch02-getting-started.md §Your first window b | The value-only output formatters are `UDEC_`, `SDEC_`, `UHEX_`, `SHEX_`, and `UB → Phrase as illustrative, e.g. 'value-only formatters such as `UDEC_`, `SDEC_`, `U |

## C-153: `int-event-source-miscount` — 1 site · Assembly (Part I)

- **The defect:** INT1, INT2, INT3 \| Software-triggered interrupts \| Inter-Cog signaling, priority events
- **Correct (true fact):** The 16 background events include exactly ONE interrupt-related event: Event 0 = 'An interrupt occurred', polled/waited via singular POLLINT/WAITINT. There are no separate INT1/INT2/INT3 event flags. INT1/2/3 are three interrupt LEVELS whose SOURCE is one of the 16 selectable events (via SETINT); they are event-driven, not primarily 'software-triggered.'
- **Source proof:** Silicon Doc p2-documentation.txt lines 5112-5145 (16 events; Event 0 = 'An interrupt occurred'); lines 5154/5210 (POLLINT/WAITINT singular)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.4.1 line 344 (even | INT1, INT2, INT3 \| Software-triggered interrupts \| Inter-Cog signaling, priori → The interrupt-related event source is a single 'INT — an interrupt occurred' (Ev |

## C-154: `integer-division-truncation-miscomment` — 1 site · IOSP

- **The defect:** 65536 * 2 / 3 = 43691 (240 degree phase word).
- **Correct (true fact):** Spin2 '/' truncates: 131072/3 = 43690 remainder 2, so the code assigns 43690, not 43691. (The rounded value would be 43691, but Spin2 does not round.)
- **Source proof:** Spin2 v55 integer '/' is truncating; computed: (65536*2)//3 = 131072//3 = 43690 (verified via python; pnut-ts '/' truncates toward zero)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-08-nco-frequency | 65536 * 2 / 3 = 43691 (240 degree phase word). → ' 43690' — the comment must state 43690, the value the truncating division actua |

## C-155: `interrupt-priority-inverted` — 1 site · Assembly (Part I)

- **The defect:** Level 3 can interrupt level 2; level 2 can interrupt level 1; level 1 can interrupt normal execution.
- **Correct (true fact):** INT1 has the highest priority and can interrupt INT2 and INT3. INT2 has middle priority and can interrupt INT3. INT3 has the lowest priority and can only interrupt non-interrupt code.
- **Source proof:** Silicon Doc p2-documentation.txt lines 5478-5480

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.4.2 / §5.4.5 line  | Level 3 can interrupt level 2; level 2 can interrupt level 1; level 1 can interr → INT1 is the highest priority and can interrupt INT2 and INT3; INT2 (middle) can  |

## C-156: `invert-output-initial-state-contradiction` — 1 site · IOSP

- **The defect:** After WRPIN(...P_TRANSITION \| P_OE \| P_INVERT_OUTPUT) and PINLOW, DE starts low (disabled).
- **Correct (true fact):** With P_OE the output is driven regardless of DIR; the transition-mode idle/reset output is low internally, and P_INVERT_OUTPUT inverts it, so the PIN is driven HIGH after setup — DE is enabled (high), not low/disabled.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 92-94 (P_OE: 'x1 = output enabled, regardless of DIR') + line 366 (transition reset output low); Spin2 v55 line 1499 (P_INVERT_OUTPUT inverts output).

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §7.7 Example 2 (RS-485 Transmit Disable Dela | After WRPIN(...P_TRANSITION \| P_OE \| P_INVERT_OUTPUT) and PINLOW, DE starts lo → Because of P_INVERT_OUTPUT, DE is HIGH (enabled) immediately after setup, not lo |

## C-157: `jump-unit-terminology-inconsistency` — 1 site · DeSilva

- **The defect:** jmp #$+8 jumps forward '8 instructions' while the adjacent jmp #$-4 jumps '4 longs (addresses)'
- **Correct (true fact):** In cog space, $-4 and $+8 both count LONGS, which equal instructions one-for-one; both comments are individually correct but the document uses two different unit words ('longs (addresses)' vs 'instructions') for the same $-relative construct on consecutive lines.
- **Source proof:** v35 CSV / Silicon Doc: in cog memory PC is long-granular (1 long = 1 instruction); jmp #target is an absolute address, $ is the current address

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Chapter 3, 'Unconditional Jumps / Relative j | jmp #$+8 jumps forward '8 instructions' while the adjacent jmp #$-4 jumps '4 lon → Use one consistent unit, e.g. 'jmp #$-4  ' Jump back 4 longs (= 4 instructions)' |

## C-158: `line-count-inconsistency` — 1 site · DeSilva

- **The defect:** A 2D point rotation takes 3 lines
- **Correct (true fact):** The worked example immediately below the heading uses 4 instructions and the prose explicitly states 'Four lines.' The heading's '3 Lines' contradicts both.
- **Source proof:** self: code block lines 2165-2170 (setq/qrotate/getqx/getqy = 4 instructions) and prose line 2172 ('*Four lines*, and a 2D rotation is done')

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch7 The Hook heading | A 2D point rotation takes 3 lines → The heading should read '4 Lines' to match the 4-instruction example and the 'Fo |

## C-159: `linesize-unit-halfpixels` — 1 site · Debug Window

- **The defect:** LINESIZE argument is in pixels (Line thickness), default 3.
- **Correct (true fact):** Spin2 v55 explicitly states LINESIZE is measured in HALF-pixels (deliberately distinguished from DOTSIZE, which is in pixels).
- **Source proof:** Spin2 v55: 'LINESIZE 0_to_32 \| Set the line size in half-pixels for connecting sample points. \| 3' (vs 'DOTSIZE ... dot size in pixels').

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch07-scope.md §config table / line 58 | LINESIZE argument is in pixels (Line thickness), default 3. → LINESIZE sets the connecting-line thickness in half-pixels, 0–32 (default 3 = 1. |

## C-160: `logic-c-parity-overgeneralization` — 1 site · Assembly (Part I)

- **The defect:** Logical instructions set C based on parity.
- **Correct (true fact):** AND/OR/XOR/TEST set C = parity, but NOT sets C = !S[31] (inverse of MSB), not parity — yet NOT is listed as a logic instruction in the same §3.4.2 table.
- **Source proof:** v35 CSV row 59 NOT 'C = !S[31]' (not parity); AND/OR/XOR rows 50/52/53 'C = parity of result'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.4.2 line 299 | Logical instructions set C based on parity. → Most logical instructions (AND, OR, XOR) set C to parity, but NOT sets C to the  |

## C-161: `logic-keyword-defaults-copied-from-scope` — 1 site · Debug Window

- **The defect:** LINESIZE default 3, range 1–32
- **Correct (true fact):** For LOGIC, LINESIZE range is 1_to_7 with default 1. The 0_to_32 / default-3 figures belong to the SCOPE table (line 1156, in half-pixels).
- **Source proof:** Spin2 v55 line 1127: 'LINESIZE 1_to_7 \| Set the line size. \| 1' (LOGIC table)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md config-keyword table, line 62  | LINESIZE default 3, range 1–32 → LINESIZE: default 1, range 1–7 (LOGIC). |

## C-162: `logic-keyword-set-overgeneralization` — 1 site · Debug Window

- **The defect:** DOTSIZE is a LOGIC creation-line keyword (default 0, range 0–32)
- **Correct (true fact):** DOTSIZE does NOT appear in the LOGIC instantiation keyword set; it is a SCOPE keyword ('DOTSIZE 0_to_32 \| ... showing exact sample points \| 0'). LOGIC's keyword set is TITLE, POS, SAMPLES, SPACING, RATE, LINESIZE, TEXTSIZE, COLOR, name/RANGE, packed_data_mode, HIDEXY.
- **Source proof:** Spin2 v55 lines 1121-1133 (LOGIC Instantiation table) vs line 1155 (SCOPE table)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md config-keyword table, line 61  | DOTSIZE is a LOGIC creation-line keyword (default 0, range 0–32) → Remove DOTSIZE from the LOGIC keyword table — it is a SCOPE-only keyword and LOG |

## C-163: `loop-body-instruction-count-overstated` — 1 site · Assembly (Part I)

- **The defect:** This pattern achieves one rotation result every ~20 instructions (the loop body)
- **Correct (true fact):** The steady-state loop body (lines 118-123) is GETQX, GETQY, WRLONG, WRLONG, CALL #queue_rotation, DJNZ; queue_rotation expands to RDLONG, RDLONG, SETQ, QROTATE, RET — roughly 11-12 instructions per result, not ~20.
- **Source proof:** This doc, code listing lines 118-140 (loop body + queue_rotation helper)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.1.6 line 143 | This pattern achieves one rotation result every ~20 instructions (the loop body) → The loop body is about a dozen (~11-12) instructions per rotation result, not ~2 |

## C-164: `lut-default-palette-mischaracterized` — 1 site · Debug Window

- **The defect:** If you select a LUT mode without defining a palette, the palette is uninitialized and LUT-mode pixels render as garbage — you must supply one with LUTCOLORS.
- **Correct (true fact):** LUTCOLORS has a documented default of 'default colors 0..7' — entries 0..7 are preloaded with default colors when no palette is supplied, so low-index LUT pixels do NOT render as garbage.
- **Source proof:** Spin2 v55 text, BITMAP Instantiation table, LUTCOLORS row: Default column = 'default colors 0..7' (spin2-v55-text.txt ~line 1330)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch04-bitmap.md §Color modes / Palette (LUT)  | If you select a LUT mode without defining a palette, the palette is uninitialize → Without LUTCOLORS the LUT palette holds default colors in entries 0..7, so low-i |

## C-165: `lut-mode-packing-mismatch` — 1 site · Debug Window

- **The defect:** With a LUT2 (two-bit) color mode you would pack with LONGS_2BIT; with a one-bit source you can drive a two-color image using LONGS_1BIT — while the following example uses `BITMAP ... LUT2 LONGS_1BIT`.
- **Correct (true fact):** v55 examples pair each LUT depth with the matching bit-width packing (LUT1↔LONGS_1BIT, LUT2↔LONGS_2BIT, LUT4↔LONGS_4BIT, LUT8↔LONGS_8BIT). LUT2 LONGS_1BIT compiles (syntactically legal).
- **Source proof:** Spin2 v55 text lines 1322 (LUT2 LONGS_2BIT) and 1375 (lut1 longs_1bit / lut2 longs_2bit ... width-matched pairings); pnut-ts compiled the LUT2 LONGS_1BIT example clean

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch13-packed-data.md §How to send packed data | With a LUT2 (two-bit) color mode you would pack with LONGS_2BIT; with a one-bit  → Either present the width-matched pairing (LUT2 → LONGS_2BIT, and for a one-bit t |

## C-166: `misquoted-source-operator` — 1 site · Assembly (Part I)

- **The defect:** CSV v35 documents this as "Z = Z AND (Result = 0)".
- **Correct (true fact):** The CSV uses '== 0' (double equals, lowercase 'result'), not '= 0'. The quoted 'Result = 0' misrepresents the source's operator.
- **Source proof:** v35 CSV rows 11/13/15/17/19/21: literal text 'Z = Z AND (result == 0)'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.2.2 line 96 | CSV v35 documents this as "Z = Z AND (Result = 0)". → CSV v35 documents this as 'Z = Z AND (result == 0)'. |

## C-167: `mode-behavior-terminology-confusion` — 1 site · IOSP

- **The defect:** P_PULSE outputs 'a specified number of transitions'.
- **Correct (true fact):** Pulse mode (%00100) counts Y pulses/cycles (Y decrements per pulse); it is the separate transition mode (%00101) whose Y counts output transitions.
- **Source proof:** Silicon Doc part4-smart-pins.txt L313-327 (%00100 pulse/cycle output): 'the pin will begin outputting a high pulse or cycles ... After each pulse, Y is decremented by one, until it reaches zero'; contrast %00101 L351-359 'transition output ... toggling for Y transitions'.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-f-mode-reference.md, Mode %00100 P_ | P_PULSE outputs 'a specified number of transitions'. → P_PULSE outputs a specified number of pulses/cycles (counted by Y), with configu |

## C-168: `mode-field-alt-bit-notation` — 1 site · Streamer

- **The defect:** D[19:16] field for RFBYTE 1-pin mode is `%pppp` (implying four pin-select bits).
- **Correct (true fact):** The D[19:16] pattern for RFBYTE 1-pin is `pppa`: D[19:17] = 3-bit pin offset, D[16] = alternate bit-order bit — only three pin-select bits, not four.
- **Source proof:** Silicon Doc v35 streamer mode table (p2-documentation.txt L3132 '%1000 ... pppa' for RFBYTE 1-pin; L3302 'pppa' for capture 1-pin) — the low bit of D[19:16] is the 'a' (alt bit-order) bit, not a pin bit.

| Document | Location | before → after |
|----------|----------|----------------|
| Streamer | streamer-body.md Appendix A, line 1469 (and  | D[19:16] field for RFBYTE 1-pin mode is `%pppp` (implying four pin-select bits). → Show D[19:16] as `%ppp_a` (or `%pppa`) — three pin-offset bits plus the D[16] al |

## C-169: `mul-16x16-mischaracterization` — 1 site · DeSilva

- **The defect:** MUL computes x = x * y, keeping the low 32 bits of the product
- **Correct (true fact):** MUL multiplies only the LOW 16 BITS of each operand (D[15:0] * S[15:0]) into a full 32-bit product. It is not 'x*y then keep low 32 bits' — for operands exceeding 16 bits the result differs entirely from the true product.
- **Source proof:** v35 CSV row 137 MUL: 'D = unsigned (D[15:0] * S[15:0]). Z = (S == 0) \| (D == 0).' (2 clocks)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Chapter 3, 'Math Without Tears', line 971 | MUL computes x = x * y, keeping the low 32 bits of the product → mul x, y  ' x = x[15:0] * y[15:0]  (unsigned 16x16 -> 32-bit product) |

## C-170: `mul-16x16-mischaracterized-as-truncated-32x32` — 1 site · DeSilva

- **The defect:** MUL gives only low 32 bits; for the full 64-bit result you must use QMUL; the high word is silently discarded by MUL
- **Correct (true fact):** MUL multiplies only the low 16 bits of each operand, so the full product fits in 32 bits — there is no wider product and no 'high word' to discard. A 64-bit result requires QMUL because QMUL is a 32x32 multiply, not because MUL truncates.
- **Source proof:** v35 CSV row 137 (MUL): 'D = unsigned (D[15:0] * S[15:0]). Z = (S == 0) \| (D == 0).'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch5 Common Gotchas i | MUL gives only low 32 bits; for the full 64-bit result you must use QMUL; the hi → MUL multiplies the low 16 bits of each operand into a complete 32-bit product (n |

## C-171: `muldiv64-every-calculation-overclaim` — 1 site · IOSP

- **The defect:** Every frequency and duty calculation in this chapter uses MULDIV64().
- **Correct (true fact):** The doc's own §15.2 Period Calculation (line 91: `frequency = sysclk / single_period`) and Example 2 (line 419: `rpm := (periods * 600) / PULSES_PER_REV`) and Example 4 (lines 491/495) use plain `*` and `/`, not MULDIV64.
- **Source proof:** Internal contradiction — chapter's own examples; Spin2 v55 line 566 MULDIV64 is the only 64-bit-product helper

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §15.1 MULDIV64 callout, line 44 | Every frequency and duty calculation in this chapter uses MULDIV64(). → Use MULDIV64 wherever an a*b product would overflow 32 bits; several small-value |

## C-172: `muldiv64-unsigned-signedness` — 1 site · P2AN001

- **The defect:** Below the ground reference the reading goes negative; above the supply reference it exceeds full scale. All four behaviors are correct.
- **Correct (true fact):** MULDIV64 is an UNSIGNED operation. A negative (pinRef − gioRef) is passed as a ~2^32 unsigned value, so the quotient is a huge positive number, not a negative reading.
- **Source proof:** Spin2 v55 reference L566: 'MULDIV64(mult1,mult2,divisor) : quotient \| ... return quotient (unsigned operation).'; CSV rows QMUL/QFRAC 'CORDIC unsigned'

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN001 | P2AN001.md §See It Work / Verify, line 615 | Below the ground reference the reading goes negative; above the supply reference → The base build and Recipes 1/2/4/5 compute the ratio with the UNSIGNED muldiv64, |

## C-173: `nco-word-bit-width` — 1 site · Streamer

- **The defect:** The NCO word is 31-bit, so its resolution is `sysclk / 2^31` ≈ 0.12 Hz at 250 MHz.
- **Correct (true fact):** 'it adds a 32-bit frequency value into a 32-bit phase accumulator, while masking the MSB of the original phase.' The SETXFRQ frequency value is a 32-bit word; the 1:1 ratio value is $8000_0000 (bit 31 set), which a 31-bit word could not hold.
- **Source proof:** Silicon Doc v35 p2-documentation.txt line 2748

| Document | Location | before → after |
|----------|----------|----------------|
| Streamer | streamer-body.md §3.4 line 232 | The NCO word is 31-bit, so its resolution is `sysclk / 2^31` ≈ 0.12 Hz at 250 MH → The frequency word is 32-bit (a 0-to-1 fraction where $8000_0000 = 1.0); because |

## C-174: `neighbor-pin-input-routing-missing` — 1 site · IOSP

- **The defect:** P_PERIODS_HIGHS on SIG_PIN+1 (no input routing) measures the same signal as SIG_PIN.
- **Correct (true fact):** By default a smart pin's A and B inputs read its OWN pin. Without routing, SIG_PIN+1 measures whatever is on pin SIG_PIN+1, not SIG_PIN. §15.4 (line 290, 'verified on P2 silicon') states an unrouted neighbor's B-input never rises so its window never closes.
- **Source proof:** Silicon Doc part4-smart-pins.txt lines 15-33 (default %AAAA/%BBBB = x000 = this pin's own read state); doc's own §15.4 line 290

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §15.2 duty example, line 129 | P_PERIODS_HIGHS on SIG_PIN+1 (no input routing) measures the same signal as SIG_ → Either wire the signal to both SIG_PIN and SIG_PIN+1 (state this), or route SIG_ |

## C-175: `obex-author-attribution` — 1 site · P2AN002

- **The defect:** "...a complete open library (SaucySoliton's FFT/IFFT, OBEX #5361)..." (repeated line 369: 'OBEX #5361 — FFT/IFFT (SaucySoliton)')
- **Correct (true fact):** The authoritative OBEX index records OBEX #5361's author as 'James Smith', not 'SaucySoliton'.
- **Source proof:** p2kb_obex_get '5361' => object_id 5361, title 'FFT IFFT', author 'James Smith'. (Object ID and 'real-input FFT' description match the doc; only the author name differs.)

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN002 | P2AN002.md §Going Further + Resources, lines | "...a complete open library (SaucySoliton's FFT/IFFT, OBEX #5361)..." (repeated  → Attribute OBEX #5361 to the name the OBEX record carries ('James Smith'), unless |

## C-176: `off-by-one-limit` — 1 site · DeSilva

- **The defect:** Keep label names under 30 characters for tool compatibility.
- **Correct (true fact):** The hard limit is 30 characters inclusive — only symbols exceeding 30 characters are rejected; exactly 30 is legal.
- **Source proof:** pnut_ts 1.55.0: a 44-char label errors 'Symbol exceeds 30 characters'; a 30-char label compiles

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Common Gotchas, lin | Keep label names under 30 characters for tool compatibility. → Keep label names to 30 characters or fewer (the compiler rejects only names long |

## C-177: `packed-logic-channel-distribution` — 1 site · Debug Window

- **The defect:** with two channels declared, the host unpacks the first long as 32 samples of channel 0 and the next long as 32 samples of channel 1.
- **Correct (true fact):** The v55 LOGIC example declares two channels ('TX' 'IN') with LONGS_2BIT and states each long yields '16 sets per long' where each 2-bit set is ONE time-sample carrying both channels' bits — i.e. the packed sub-values are distributed per-sample across the declared channels, not one whole element per channel.
- **Source proof:** Spin2 v55 text lines 1143-1144 (LOGIC packed-data worked example)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch13-packed-data.md §intro, lines 104-107 | with two channels declared, the host unpacks the first long as 32 samples of cha → In a multi-channel LOGIC display, the sub-values unpacked from a packed element  |

## C-178: `pasm-immediate-label-address-vs-pin-value` — 1 site · IOSP

- **The defect:** The example configures a smart-pin edge counter on EVENT_PIN (pin 20), using dirl/wrpin/wxpin/wypin/dirh/rdpin with #EVENT_PIN as the pin operand while EVENT_PIN is defined as `EVENT_PIN long 20`.
- **Correct (true fact):** `EVENT_PIN long 20` makes EVENT_PIN a cog register at a low address holding the value 20. `#EVENT_PIN` (immediate) resolves to that register's ADDRESS, not 20. All the smart-pin setup instructions therefore target the pin numbered by EVENT_PIN's cog address, not pin 20. To target pin 20 the example must either declare `EVENT_PIN = 20` in CON (then `#EVENT_PIN` = 20) or read the register with `... 
- **Source proof:** pnut_ts v1.55.0 compile of the fragment (compiles, but semantics): a DAT symbol's value is its cog-RAM address; `#EVENT_PIN` is the immediate cog address of the long, not its stored value 20

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-14-counting.md §1 | The example configures a smart-pin edge counter on EVENT_PIN (pin 20), using dir → Declare EVENT_PIN as a CON constant (EVENT_PIN = 20) so `#EVENT_PIN` is the pin  |

## C-179: `pasm-immediate-label-address-vs-value` — 1 site · IOSP

- **The defect:** PASM2 example configures pin 20 for 100 kHz PWM; PWM_PIN is defined as `long 20` and used as `#PWM_PIN` in dirl/wrpin/wxpin/dirh/wypin.
- **Correct (true fact):** The `#` prefix makes the operand an immediate equal to the SYMBOL'S ADDRESS. Because PWM_PIN is a DAT long (at cog address ~12 in this program), `#PWM_PIN` = 12, not the contents 20. Every smart-pin op (dirl/wrpin/wxpin/dirh/wypin) therefore targets pin ~12, not pin 20; the literal 20 stored in the long is never used as a pin number.
- **Source proof:** pnut_ts 1.55.0 compile+listing: `dirl #PWM_PIN` with `PWM_PIN long 20` emits D=1 (the symbol's cog address), whereas `dirl #20` emits D=20 (od bytes 40 02 64 fd vs 40 28 64 fd).

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §9.7 Example 4 (PASM2 High-Frequency PWM), l | PASM2 example configures pin 20 for 100 kHz PWM; PWM_PIN is defined as `long 20` → Define the pin as a CON symbol (`PWM_PIN = 20`) so `#PWM_PIN` is the immediate v |

## C-180: `pasm-rev-needs-shl-first` — 1 site · IOSP

- **The defect:** A bare `rev data` reverses the data bits for MSB-first sync transmission
- **Correct (true fact):** PASM REV reverses all 32 bits; to MSB-first an 8-bit value you must SHL D,#32-8 THEN REV D, otherwise the byte lands in the high bits and the LSB-first shifter emits zeros.
- **Source proof:** Silicon Doc p2-documentation.txt lines ~9061-9062 (%11100 sync serial transmit): 'If you intend to send MSB-first data, you must first shift and then reverse it ... do a SHL D,#32-8 and then a REV D'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | A bare `rev data` reverses the data bits for MSB-first sync transmission → shl data,#32-8   'left-justify the byte\n rev data          'then reverse into l |

## C-181: `pasm2-label-addr-as-immediate-pin` — 1 site · IOSP

- **The defect:** Example 4 configures/transmits on TX_PIN (pin 20) via dirl/wrpin/wxpin/testp/wypin #TX_PIN
- **Correct (true fact):** TX_PIN is a DAT long, so the immediate '#TX_PIN' evaluates to the label's cog address (18), NOT the stored value 20. The 'long 20' is never read. All pin ops in Example 4 therefore act on pin 18, not the intended pin 20.
- **Source proof:** pnut-ts -l listing of Example 4: 'DAT_LONG VALUE: 01200048 NAME: TX_PIN' → TX_PIN resolves to cog register address $12 = 18. Spin2 v55 note (line 39): '#register now returns the register's address.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | Example 4 configures/transmits on TX_PIN (pin 20) via dirl/wrpin/wxpin/testp/wyp → Define the pin as a CON (e.g. 'TX_PIN = 20' in a CON block) so '#TX_PIN' is the  |

## C-182: `pin-config-bits-mislabel` — 1 site · IOSP

- **The defect:** the DAC_MODE bits (P[12:10]=%101)
- **Correct (true fact):** The pin-configuration bits are the M[12:0] bits (WRPIN D[20:8]); DAC_MODE is selected by M[12:10]=%101, consistently written 'M', never 'P'.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 97, 108-113, 237, 255, 286

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-4-special-modes/chapter-18-repository.m | the DAC_MODE bits (P[12:10]=%101) → the DAC_MODE bits (M[12:10]=%101) ... |

## C-183: `pin-latency-propagation-vs-pipeline` — 1 site · IOSP

- **The defect:** Total latency from instruction start to pin transition: 5 clock cycles (2 for instruction execution + 3 pipeline delay).
- **Correct (true fact):** The 3 extra clocks are three output-register/synchronizer stages between the OUTx/DIRx bit and the pad; the silicon frames them as pin registration/propagation, not instruction-pipeline latency.
- **Source proof:** Silicon Doc p2-documentation.txt lines 4967-4970 (I/O PIN TIMING): 'THREE additional clocks after the instruction before the pin starts transitioning'; diagram shows 3 REG->REG->REG output-register stages, not the instruction pipeline.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-01-direct-io.md §1.2 Output Timing,  | Total latency from instruction start to pin transition: 5 clock cycles (2 for in → Total latency is 5 clocks (2 for the instruction plus 3 clocks of pin-output pro |

## C-184: `pin-power-group-size` — 1 site · P2AN001

- **The defect:** The P2 powers its I/O pins in isolated groups of four — pins 0–3, 4–7, …, 60–63 — and each group shares one VIO/GIO supply pair.
- **Correct (true fact):** P2 I/O pins are powered/grounded in groups of EIGHT (P0-7, P8-15, … P56-63), each 8-pin group sharing one VIO/GIO pair; pin groups are addressed in 8-pin increments.
- **Source proof:** Silicon Doc p2-documentation.txt L511-517/L533-534 (VIO_{x}_{y}='Power for smart pins {x} through {y}', GIO_{x}_{y}='Ground for smart pins {x} through {y}'); L3606 ('%ppp ... select the pin group, in 8-pin increments')

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN001 | P2AN001.md §Pitfalls & Notes, line 632 | The P2 powers its I/O pins in isolated groups of four — pins 0–3, 4–7, …, 60–63  → The P2 powers its I/O pins in isolated groups of EIGHT — pins 0–7, 8–15, …, 56–6 |

## C-185: `pinclear-wrpin0-equivalence` — 1 site · IOSP

- **The defect:** PINCLEAR(pin) — or equivalently WRPIN(pin, 0) — clears all enhanced configuration and smart pin modes, returning the pin to basic Direct I/O operation.
- **Correct (true fact):** PINCLEAR performs TWO operations: DIR=0 (holds pin in reset / makes it an input) AND THEN WRPIN=0. A bare WRPIN(pin,0) only rewrites the mode register and leaves the DIR bit unchanged (the pin can remain a driven output).
- **Source proof:** Spin2 v55 ref line 538: 'PINCLEAR(PinField) \| Clear PinField smart pin(s): DIR=0, then WRPIN=0.'; silicon-doc part4-smart-pins line 179 'To return a pin to normal mode, do a WRPIN #0,pin'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-1-fundamentals/chapter-02-enhanced-dire | PINCLEAR(pin) — or equivalently WRPIN(pin, 0) — clears all enhanced configuratio → PINCLEAR(pin) clears the pin's mode AND lowers DIR (DIR=0, then WRPIN=0); WRPIN( |

## C-186: `pinfield-range-order-reversed` — 1 site · IOSP

- **The defect:** PINLOW(PHASE_A..PHASE_C) enables pins 10,11,12 simultaneously.
- **Correct (true fact):** The range is written high-pin..low-pin (Top..Bottom). PHASE_A..PHASE_C = 10..12 has Top(10) < Bottom(12), so it WRAPS: base=12, extra=(10-12) mod 32 = 30 additional pins -> a 31-pin wrapped field, NOT pins 10..12.
- **Source proof:** Spin2 v55 text lines 385-393: pinfield range is 'Top..Bottom' (e.g. PINLOW(49..40) = pins 49..40), 'wraps if Top < Bottom'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-08-nco-frequency | PINLOW(PHASE_A..PHASE_C) enables pins 10,11,12 simultaneously. → Write the range descending: PINLOW(PHASE_C..PHASE_A) i.e. 12..10, which yields b |

## C-187: `pipeline-data-hazard-fabrication` — 1 site · DeSilva

- **The defect:** 'Bad: result needed immediately' add x,y then cmp x,#10 wcz — 'Stall waiting for x'; interleaving a mov avoids a pipeline stall on the data dependency.
- **Correct (true fact):** When the pipeline is full each instruction takes as little as two clocks; extra clocks come only from multi-cycle (e.g. hub) instructions whose stall propagates, cancelled conditionals (still 2 clocks), and branch flushes. No data-dependency/register-forwarding stall is described — using an ALU result in the immediately following instruction does not stall.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 628-631 (five-stage pipeline description)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.12 'Pipeline-Awar | 'Bad: result needed immediately' add x,y then cmp x,#10 wcz — 'Stall waiting for → On the P2 a register result is available to the next instruction with no stall;  |

## C-188: `pollqmt-misused-as-ready-check` — 1 site · Assembly (Part I)

- **The defect:** For non-blocking result checking, use POLLQMT to test whether the CORDIC pipeline is empty
- **Correct (true fact):** The QMT flag is 'Set whenever GETQX/GETQY executes without any CORDIC results available or in progress' — an edge event recording a past read-while-empty. It is NOT a live 'pipeline empty / result pending' status pollable before reading to decide whether a result is ready.
- **Source proof:** Silicon Doc p2-documentation.txt line 5401; v35 CSV row 286 (POLLQMT: 'Get QMT event flag into C/Z, then clear it')

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.1.5 lines 85-91 | For non-blocking result checking, use POLLQMT to test whether the CORDIC pipelin → POLLQMT reports whether a GETQX/GETQY has already executed with no result availa |

## C-189: `precalc-nco-value-off-by-one` — 1 site · IOSP

- **The defect:** At 300 MHz the NCO Y Value for 10 kHz is 143,165.
- **Correct (true fact):** The exact value is 143165.58, which under round-to-nearest (the convention every other cell in these tables uses, e.g. 1000 Hz -> 21474.8 -> 21,475) is 143,166, not 143,165.
- **Source proof:** Arithmetic against the appendix's own NCO formula (line 42): Y = (frequency × 2^32) / sysclk; (10000 × 4294967296) / 300000000 = 143165.5765

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-c-formulas-refere | At 300 MHz the NCO Y Value for 10 kHz is 143,165. → At 300 MHz the NCO Y Value for 10 kHz should be 143,166. |

## C-190: `precise-default-inverted` — 1 site · Debug Window

- **The defect:** the window keeps sub-pixel precision (1/256 of a pixel) by default; PRECISE flips between sub-pixel mode (the default) and whole-pixel mode
- **Correct (true fact):** Precise mode is DISABLED by default; PRECISE toggles it ON so that DOT/LINE size and (x,y) are expressed in 256ths of a pixel.
- **Source proof:** Spin2 v55 text.txt line 1271: PRECISE \| Toggle precise mode ... expressed in 256ths of a pixel. \| Default: disabled

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch05-plot.md §The update model / PRECISE, li | the window keeps sub-pixel precision (1/256 of a pixel) by default; PRECISE flip → By default PRECISE mode is off (coordinates in whole pixels); issuing PRECISE tu |

## C-191: `ptr-expression-scope-overgeneralization` — 1 site · DeSilva

- **The defect:** ptra++ only works with hub-access instructions like RDLONG.
- **Correct (true fact):** Line 107: 'RDLUT/WRLUT can now handle PTRx expressions.' RDLUT/WRLUT are lookup-RAM (not hub-access) instructions and accept PTRx (/P) operands including ptra++ updating expressions. So PTRx-updating expressions are not exclusive to hub-access instructions.
- **Source proof:** Silicon Doc v35 p2-documentation.txt line 107; CSV rows 151/220 syntax 'RDLUT D,{#}S/P' and 'WRLUT {#}D,{#}S/P'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.12 'Unrolling Loo | ptra++ only works with hub-access instructions like RDLONG. → PTRx auto-updating expressions (ptra++) work with hub RD/WR instructions and als |

## C-192: `ptr-index-must-be-constant` — 1 site · DeSilva

- **The defect:** rdlong width, ptra[index] — reads each servo's pulse width using the runtime loop counter 'index' as the PTRA offset
- **Correct (true fact):** A PTRx index is a compile-time constant encoded in the S field — it cannot be a runtime register value; the assembler bakes in the symbol's value at assembly time.
- **Source proof:** Silicon Doc lines 6924-6963 (PTR expression: 5-bit scaled index / 20-bit unscaled index encoded in the instruction), 7153. pnut-ts 1.55: `rdlong width, ptra[index]` compiles but encodes the symbol 'index' (its compile-time cog address) as a FIXED index.

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.11 servo example  | rdlong width, ptra[index] — reads each servo's pulse width using the runtime loo → To index by a runtime counter, compute the address into PTRA (or a temp) first;  |

## C-193: `ptra-label-vs-code-mismatch` — 1 site · DeSilva

- **The defect:** Read data with FIFO, process, write via PTRA ... wrlong input, dest_ptr ' Write result via PTRA
- **Correct (true fact):** The example's block/header comments (L3114, L3124) claim writes go 'via PTRA', but the code uses a normal register dest_ptr with an explicit 'add dest_ptr, #4' — it does not use the PTRA hardware pointer or its auto-increment. The your-turn example at L3170 correctly demonstrates PTRA (ptra++).
- **Source proof:** Doc-internal: L3116 'mov dest_ptr, ##dest' + L3125 'add dest_ptr, #4' show a plain register manually incremented, not the PTRA hardware pointer; contrast L3170 'wrlong result, ptra++' which does use PTRA

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md ch.9 'Processing Pip | Read data with FIFO, process, write via PTRA ... wrlong input, dest_ptr ' Write  → Either label the write as 'via manual pointer dest_ptr', or change the code to u |

## C-194: `ptrb-not-a-user-parameter` — 1 site · DeSilva

- **The defect:** rdlong delay, ptrb reads a per-cog 'delay' parameter passed to the cog via PTRB
- **Correct (true fact):** COGINIT sets PTRB = the code load/start address (PASMaddr) and PTRA = the single passed parameter (SETQ value / Spin2 coginit's 3rd arg). PTRB is the code pointer, not a second user parameter; reading it returns the address of (i.e. points at) the loaded PASM code, not a delay value.
- **Source proof:** Silicon Doc v35 lines ~792-800 (COGINIT): S/# 'will be written into the target cog's PTRB register'; PTRA is loaded from a preceding SETQ (the passed parameter). Register map line 360: PTRB = 'Code pointer passed from COGINIT', PTRA = 'Data pointer passed from COGINIT'. Spin2 line 517: COGINIT(CogNu

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Ch2 §Your Turn Experiment 2 'Parallel Patter | rdlong delay, ptrb reads a per-cog 'delay' parameter passed to the cog via PTRB → Only one parameter is passed (in PTRA). To pass both a pin and a delay, point PT |

## C-195: `pulse-retrigger-timing-immediate` — 1 site · IOSP

- **The defect:** When Y = 0 (idle), writing a new Y value triggers a new pulse sequence immediately.
- **Correct (true fact):** Any non-zero Y write begins output at the NEXT base period boundary, not immediately — the silicon doc draws no immediate-vs-deferred distinction between the idle (Y=0) and running (Y>0) cases.
- **Source proof:** Silicon Doc v35, part4-smart-pins.txt line 326: 'Whenever Y[31:0] is written with a non-zero value, the pin will begin outputting a high pulse or cycles, starting at the next base period.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §7.2 Retriggering, line 129 | When Y = 0 (idle), writing a new Y value triggers a new pulse sequence immediate → Writing a non-zero Y (whether from idle or mid-sequence) starts pulse output at  |

## C-196: `pwm-dither-tone-fixed-not-period-scaled` — 1 site · P2AN003

- **The defect:** Raising the period lowers the sample rate (and the dither frequency)
- **Correct (true fact):** For PWM dither the spectral tone is fixed at Fclock/256 because the PWM completes its dither pattern every 256 clocks; this does NOT depend on the sample period. Raising the sample period lowers only the sample rate (Fclock/period), not the dither tone frequency.
- **Source proof:** silicon-doc/part4-smart-pins.txt line 290-302 (%00011 PWM dither): sample period must be a multiple of 256; 'a maximum of only two transitions occur for every 256 clocks... a frequency of Fclock/256 will be present in the output at -48dB'

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN003 | P2AN003.md §Pitfalls & Notes, 'Tip — the sam | Raising the period lowers the sample rate (and the dither frequency) → Raising the period lowers the sample rate; the PWM dither tone stays fixed at sy |

## C-197: `pwm-mode-frame-formula-inconsistency` — 1 site · IOSP

- **The defect:** For 20 kHz motor control, frame period = sysclk/freq = 200,000,000 / 20,000 = 10,000.
- **Correct (true fact):** Frame for a 20 kHz motor depends on mode: triangle needs sysclk/(2·freq)=5,000; sawtooth needs sysclk/freq=10,000. §9.6 states 10,000 with no mode named, while the chapter's motor example (Example 3) uses triangle and computes 5,000 for the identical 20 kHz target.
- **Source proof:** This document §9.7 Example 3, line 492: for the SAME 20 kHz motor, `frame_period := _clkfreq / (2 * PWM_FREQ)` = 5,000 (triangle). Silicon Doc part4-smart-pins.txt line 440: triangle update time is TWO frame periods × base.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §9.6 Choosing Parameters, lines 398-403 (mot | For 20 kHz motor control, frame period = sysclk/freq = 200,000,000 / 20,000 = 10 → State the mode: for a triangle-driven motor at 20 kHz, frame = sysclk/(2·20000)  |

## C-198: `pwm-output-edge-mischaracterization` — 1 site · IOSP

- **The defect:** The sawtooth pattern creates a fast rising edge and slow falling edge in the output.
- **Correct (true fact):** The smart-pin sawtooth OUTPUT is a digital PWM pulse: high while the captured value ≥ counter, low otherwise — both transitions are sharp digital edges. The "fast/slow edge" asymmetry belongs to the internal COUNTER ramp (fast reset, slow rise), not to the pin output.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt:471-472 (sawtooth output: "If it is equal or greater, a high is output. If it is less, a low is output.")

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-09-pwm-output.md | The sawtooth pattern creates a fast rising edge and slow falling edge in the out → The output is a rectangular PWM pulse with sharp edges in both directions; it is |

## C-199: `pwm-period-field-overflow` — 1 site · DeSilva

- **The defect:** For a 1 kHz PWM at 160 MHz, period = 160,000 (to be written via the wxpin ##period model)
- **Correct (true fact):** The PWM base period field X[15:0] is 16 bits (max 65,535 clocks); a 160,000-clock period cannot be expressed as a single base-period value and must be decomposed into base period × frame period
- **Source proof:** Silicon Doc v35 (p2-documentation.txt L8002): PWM-sawtooth 'X[15:0] establishes a base period' — a 16-bit field (max 65,535)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch14 'Your Turn' Ex | For a 1 kHz PWM at 160 MHz, period = 160,000 (to be written via the wxpin ##peri → 160,000 clocks (1 kHz @160 MHz) exceeds the 16-bit base-period field; realize it |

## C-200: `pwm-resolution-bit-mislabel` — 1 site · IOSP

- **The defect:** Frame period = 2000 (from `##$07D0_0001`) provides "10-bit resolution".
- **Correct (true fact):** By the doc's own log2(frame) resolution formula, frame=2000 yields ~11-bit resolution; a true 10-bit frame is 1024 (per the §9.6 table).
- **Source proof:** This document §9.6 line 401 states the resolution rule: `Actual resolution = log2(frame)`. log2(2000) = 10.97 ≈ 11 bits, and §9.6 table (line 388) maps 1024→10-bit, not 2000.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §9.7 Example 4 comment, line 526 | Frame period = 2000 (from `##$07D0_0001`) provides "10-bit resolution". → Frame=2000 gives roughly 11-bit resolution (log2(2000)≈11.0); either call it ~11 |

## C-201: `pwm-xregister-oversimplification` — 1 site · DeSilva

- **The defect:** PWM sawtooth period is set by wxpin ##period as a single 'Period in clocks' value
- **Correct (true fact):** PWM-sawtooth X is two 16-bit fields: base period (X[15:0]) and frame period in base-periods (X[31:16]). A single value written as 'period in clocks' sets X[31:16] (frame period) from its high bits, and a small value leaves frame period = 0, which never produces PWM
- **Source proof:** Silicon Doc v35 (p2-documentation.txt L8002-8003, PWM sawtooth): 'X[15:0] establishes a base period in clock cycles... X[31:16] establishes a PWM frame period in terms of base periods'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch14 'PWM Output' l | PWM sawtooth period is set by wxpin ##period as a single 'Period in clocks' valu → WXPIN sets base period in X[15:0] and PWM frame period in X[31:16]; the value mu |

## C-202: `q-register-mislabeled-flag` — 1 site · DeSilva

- **The defect:** Q is a flag alongside C and Z.
- **Correct (true fact):** "The SETQ and SETQ2 instructions write to the Q register" — Q is a 32-bit value register (used by block RDLONG/WRLONG, QDIV/QFRAC/QROTATE CORDIC, XORO32, RDLUT, streamer NCO), not a single-bit C/Z-style status flag.
- **Source proof:** Silicon Doc p2-documentation.txt line 2522 (SETQ CONSIDERATIONS)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §The Flags header, l | Q is a flag alongside C and Z. → Q is a 32-bit register set with SETQ/SETQ2 (not a C/Z-style flag); CORDIC is one |

## C-203: `q-register-not-flag` — 1 site · DeSilva

- **The defect:** The Q flag is special - it's used by CORDIC operations (Chapter 7).
- **Correct (true fact):** Q is a 32-bit register (set by SETQ), used as an extra operand for block transfers and some CORDIC ops (QDIV/QFRAC/QROTATE) — it is NOT a single-bit condition flag like C or Z.
- **Source proof:** Silicon Doc v35 / CSV row 313 SETQ 'Set Q to D. Use before RDLONG/WRLONG/WMLONG ... QDIV/QFRAC/QROTATE'; Q is a 32-bit value register, not a C/Z-style status bit

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md, Ch.3 'The Flags: C  | The Q flag is special - it's used by CORDIC operations (Chapter 7). → Q is a 32-bit setup register (loaded by SETQ), not a flag. It supplies an extra  |

## C-204: `qmt-semantics-empty-not-complete` — 1 site · Assembly (Part I)

- **The defect:** QMT \| CORDIC operation complete \| Math coprocessor completion
- **Correct (true fact):** Event 15 / QMT = 'GETQX/GETQY executed without any CORDIC results available or in progress' (a CORDIC-read-while-empty / underflow indicator). It does NOT signal 'operation complete.'
- **Source proof:** Silicon Doc p2-documentation.txt line 5145 (Event 15) + line 5401; v35 CSV row 286 (POLLQMT)

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.4.1 line 354 (even | QMT \| CORDIC operation complete \| Math coprocessor completion → QMT = CORDIC read-with-no-result (pipeline-empty underflow): set when GETQX/GETQ |

## C-205: `qsin-parameter-name-error` — 1 site · IOSP

- **The defect:** QSIN's third parameter is a "twist" (parameter list documented as "(length, angle, twist)") and QSIN(32767, phase, 0) is called accordingly.
- **Correct (true fact):** QSIN's parameters are (length, step, stepsInCircle). The third argument is stepsInCircle (the number of steps in a full circle; 0 means a 2^32-step circle), not a "twist". There is no "twist" parameter on QSIN.
- **Source proof:** spin2-v55-text.txt line 564: "QSIN(length, step, stepsInCircle) : y \| ... Use 0 for stepsInCircle = $1_0000_0000. stepsInCircle is unsigned."

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-10-dac-output.md §10.8 Example 2, li | QSIN's third parameter is a "twist" (parameter list documented as "(length, angl → The CORDIC sine call parameters are (length, step, stepsInCircle); passing 0 for |

## C-206: `random-operator-single-vs-double-question` — 1 site · Debug Window

- **The defect:** the random-number generator — `GETRND` (or the `?` operator) for noise
- **Correct (true fact):** The Spin2 pseudo-random operator is `??` (double question mark). A single `?` is the ternary conditional operator (`x ? y : z`), not a random generator.
- **Source proof:** Spin2 v55 line 412: `?? (pre) \| ??var \| Iterate long var per XORO32, return pseudo-random value`; line 493: `? : \| x ? y : z \| If x <> 0 then return y, else return z`

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch02-getting-started.md §The no-hardware phi | the random-number generator — `GETRND` (or the `?` operator) for noise → the random-number generator — `GETRND` (or the `??` operator) for noise |

## C-207: `range-lower-bound-wrong` — 1 site · Debug Window

- **The defect:** SPACING range is 1–32
- **Correct (true fact):** SPACING range is 2_to_32 (minimum 2, not 1).
- **Source proof:** Spin2 v55 line 1125: 'SPACING 2_to_32 \| Set the sample spacing... \| 8'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md config-keyword table, line 59  | SPACING range is 1–32 → SPACING: default 8, range 2–32. |

## C-208: `range-upper-bound-off-by-one` — 1 site · Debug Window

- **The defect:** SAMPLES range is 4–2047
- **Correct (true fact):** SAMPLES range is 4_to_2048 (default 32).
- **Source proof:** Spin2 v55 line 1124: 'SAMPLES 4_to_2048 \| ... \| 32'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md config-keyword table, line 58  | SAMPLES range is 4–2047 → SAMPLES: default 32, range 4–2048. |

## C-209: `rcfast-frequency-range` — 1 site · Assembly (Part I)

- **The defect:** The RCFAST oscillator runs at ~20-30 MHz (typically ~24 MHz).
- **Correct (true fact):** The silicon consistently characterizes RCFAST as '20 MHz+' / '20+ MHz, nominally 24 MHz' — a lower bound of ~20 MHz with nominal 24; it never states an upper bound of ~30 MHz.
- **Source proof:** Silicon Doc p2-documentation.txt line 473 ('Internal 20+ MHz RC oscillator, nominally 24 MHz'), line 6045 ('a 20MHz+ (RCFAST)'), line 6220 ('20 MHz+')

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.7.1 Initial Chip S | The RCFAST oscillator runs at ~20-30 MHz (typically ~24 MHz). → RCFAST is an internal RC oscillator running 20 MHz or more, nominally ~24 MHz. T |

## C-210: `rcfast-nominal-frequency` — 1 site · DeSilva

- **The defect:** Without it, the chip runs at a sluggish ~20 MHz on its internal RC oscillator
- **Correct (true fact):** 'Internal 20+ MHz RC oscillator, nominally 24 MHz, used as initial clock source'; RCFAST is '20 MHz+ ... used on boot-up'. The nominal boot frequency is ~24 MHz (20-30 MHz range), not ~20 MHz.
- **Source proof:** Silicon Doc v35 p2-documentation.txt line 473 & 6220

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md Ch.1 'The Clock Prea | Without it, the chip runs at a sluggish ~20 MHz on its internal RC oscillator → Without a clock setup the chip runs on its internal RCFAST oscillator, spec'd at |

## C-211: `rdpin-c-in-bit31-unmasked` — 1 site · IOSP

- **The defect:** RDPIN(pin) returns the smart pin's Z register contents (displayed unmasked as UHEX_)
- **Correct (true fact):** The value returned by RDPIN() carries the smart-pin C flag in bit 31 and the Z result in bits 30:0. Bit 31 of the displayed value is NOT part of the Z data; a full 32-bit Z result loses its top bit to the C flag.
- **Source proof:** Spin2 v55 spin2-v55-text.txt L543: 'RDPIN (Pin) : Zval ... Zval[31] = C flag from RDPIN, other bits are RDPIN data'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-e-troubleshooting.md §"Debugging Te | RDPIN(pin) returns the smart pin's Z register contents (displayed unmasked as UH → RDPIN(pin) returns the Z result in bits 30:0 with the smart-pin C flag in bit 31 |

## C-212: `rdpin-reset-fabrication` — 1 site · IOSP

- **The defect:** Some modes (like totalizer counters) benefit from RQPIN for intermediate reads while RDPIN resets for the next period.
- **Correct (true fact):** RDPIN's only effect beyond returning Z is acknowledging the smart pin (lowering IN). In totalizer/continuous mode (X=0) the count 'can always be read via RDPIN/RQPIN' — it is continuous with no 'next period', and reading does not reset the accumulator. Periodic re-arm happens automatically at period end (or by pulsing DIR low), not because RDPIN was used instead of RQPIN.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 536-537, 540-543 (quadrature/counter modes) and lines 151-153 (RDPIN semantics)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-04-smart-pin-configuration.md §4.6 R | Some modes (like totalizer counters) benefit from RQPIN for intermediate reads w → RDPIN and RQPIN return the same Z value in these modes; they differ only in that |

## C-213: `register-description-imprecision` — 1 site · IOSP

- **The defect:** In NCO-duty mode Y[31:0] is a 'Frequency × duty control' (a product of frequency and duty).
- **Correct (true fact):** Y[31:0] is the single value added to the Z accumulator each base period; both output frequency and duty derive from that one added value (duty ~ Y/2^32), not from a product of two separate frequency and duty parameters.
- **Source proof:** Silicon Doc part4-smart-pins.txt L407-410 (%00111 NCO duty): 'Y[31:0] will be added into Z[31:0] at each base period. The pin output will reflect Z overflow.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-f-mode-reference.md, Mode %00111 P_ | In NCO-duty mode Y[31:0] is a 'Frequency × duty control' (a product of frequency → Y[31:0] is the frequency/duty control word added to Z each base period (a single |

## C-214: `repository-arbitration-inflation` — 1 site · IOSP

- **The defect:** These modes provide hardware-arbitrated data transfer without lock contention.
- **Correct (true fact):** The repository is a single 32-bit register: WXPIN writes it, RDPIN/RQPIN read it; concurrent RQPIN reads don't conflict. The doc describes NO write-arbitration mechanism — a later WXPIN simply overwrites.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 150-154, 224-230

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-4-special-modes/chapter-18-repository.m | These modes provide hardware-arbitrated data transfer without lock contention. → Reads are conflict-free (any number of cogs may RQPIN concurrently); writes are  |

## C-215: `resolution-range-understated` — 1 site · IOSP

- **The defect:** SINC2 Sampling nominal resolution is 8-14 bits.
- **Correct (true fact):** The silicon SINC2-Sampling resolution column spans 2 bits (2-clock period) through 14 bits (8192-clock period) — i.e. 2-14 bits, not 8-14.
- **Source proof:** silicon part4-smart-pins lines 826-853 (SINC2 Sampling 'Sample Resolution' column: 2 bits at 2 clocks up to 14 bits at 8192 clocks)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-d §Filter Modes (X[5:4]), line 183 | SINC2 Sampling nominal resolution is 8-14 bits. → Nominal SINC2-Sampling resolution ranges 2-14 bits (period-dependent); '8-14 bit |

## C-216: `rev-operand-off-by-one` — 1 site · IOSP

- **The defect:** value REV 8 reverses 8 bits for MSB-first SPI transmission
- **Correct (true fact):** REV y reverses bits 0..y INCLUSIVE, i.e. (y+1) bits. REV 8 reverses 9 bits; an 8-bit reversal requires REV 7.
- **Source proof:** Spin2 v55 ref line 448: 'REV \| x REV y \| Reverse order of bits 0..y of x and zero-extend'; pnut-ts: $FF REV 8 = $1FE, $FF REV 7 = $FF

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | value REV 8 reverses 8 bits for MSB-first SPI transmission → reversed := value REV 7   ' reverse the low 8 bits for MSB-first |

## C-217: `rev-operator-off-by-one` — 1 site · IOSP

- **The defect:** reversed := value REV 8   ' reverse the data bits for MSB-first
- **Correct (true fact):** REV y reverses bits 0..y INCLUSIVE = y+1 bits. To reverse an 8-bit value you need REV 7. REV 8 reverses 9 bits, moving the original MSB to bit 8 (outside the transmitted 8-bit field) and putting a 0 in bit 0 — the smart pin then shifts out 0,b7,b6..b1 and never sends b0.
- **Source proof:** Spin2 v55 ref line 448: 'x REV y ... Reverse order of bits 0..y of x and zero-extend'; pnut-ts constant-fold: $01 REV 8 = $100, $FF REV 8 = $1FE (9 bits); $01 REV 7 = $80, $FF REV 7 = $FF (8 bits). Silicon-doc p2-documentation.txt sync-serial-tx: MSB-first idiom is 'SHL D,#32-8 then REV D' (an 8-bit

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-11-serial-transm | reversed := value REV 8   ' reverse the data bits for MSB-first → reversed := value REV 7   ' reverse the 8 data bits for MSB-first (REV n reverse |

## C-218: `rqpin-in-flag-never-clears` — 1 site · IOSP

- **The defect:** IF PINREAD(REPO_PIN) ... ' New data available? ... display_value(RQPIN(REPO_PIN))
- **Correct (true fact):** WXPIN raises IN; IN is lowered only by an acknowledging op (WRPIN/WXPIN/WYPIN/RDPIN/AKPIN). RQPIN (read-quiet) does NOT acknowledge, so it never clears IN.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 150-154, 227

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-4-special-modes/chapter-18-repository.m | IF PINREAD(REPO_PIN) ... ' New data available? ... display_value(RQPIN(REPO_PIN) → Because RQPIN never clears IN, PINREAD(IN) cannot detect 'new' data — it stays h |

## C-219: `sample-feed-udec-vs-value` — 1 site · Debug Window

- **The defect:** udec_(x) would send the visible digits of x, which is not what a sample stream wants.
- **Correct (true fact):** The `() form is shorthand for SDEC_ — it emits signed-decimal digit TEXT, exactly as UDEC_ emits unsigned-decimal digit text. Both produce a numeric token the graphical parser reads as a sample; the parser 'treats any commas as whitespace' and reads number elements.
- **Source proof:** Spin2 v55 DEBUG-display table: "DEBUG(`MyLog SAMPLES `(v)) -> ... SAMPLES 100 \| Decimal numbers ... `(value) notation. Short for SDEC_."

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch07-scope.md §Sending samples / line 146-14 | udec_(x) would send the visible digits of x, which is not what a sample stream w → Feed samples with the `() value form. (Note: `() is itself SDEC_ digit text; the |

## C-220: `sample-period-zero-mislabel` — 1 site · IOSP

- **The defect:** WXPIN(NOISE_PIN, 0) ' No sample period
- **Correct (true fact):** 'set X[15:0] to zero (65,536 clocks), in order to maximize the unused sample period, thereby reducing switching power.' X=0 is the LONGEST period, not 'no' period.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 241-243

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-4-special-modes/chapter-18-repository.m | WXPIN(NOISE_PIN, 0) ' No sample period → WXPIN(NOISE_PIN, 0) ' Max sample period (65,536 clocks; low power) |

## C-221: `sample-rate-arithmetic-mismatch` — 1 site · IOSP

- **The defect:** This initializes the audio DAC at 44.1 kHz using WXPIN(_clkfreq / SAMPLE_RATE / 256 * 256).
- **Correct (true fact):** The rounding-to-256 expression yields a 4352-clock sample period, i.e. ~45.96 kHz, roughly 4% above the stated 44.1 kHz (rounding DOWN to the nearest 256 clocks raises the rate).
- **Source proof:** Integer arithmetic: 200_000_000 / 44100 = 4535; 4535 / 256 = 17; 17 * 256 = 4352 clocks/sample => 200_000_000 / 4352 = 45,955 Hz.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-10-dac-output.md §10.8 Example 2, li | This initializes the audio DAC at 44.1 kHz using WXPIN(_clkfreq / SAMPLE_RATE /  → State the achieved rate (~46 kHz after rounding the period to a multiple of 256) |

## C-222: `save-command-missing-argument` — 1 site · Debug Window

- **The defect:** `SAVE` (with no argument) saves the current window image to a file on the host.
- **Correct (true fact):** SAVE requires a 'filename' argument and takes an optional {WINDOW} keyword that selects the entire window vs. just the display area. The doc presents bare `SAVE` with no argument and omits the WINDOW option.
- **Source proof:** Spin2 v55 line 1392: 'SAVE {WINDOW} 'filename' \| Save a bitmap file (.bmp) of either the entire window or just the display area.'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch11-midi.md §Clearing and saving, line 153  | `SAVE` (with no argument) saves the current window image to a file on the host. → `SAVE {WINDOW} 'filename'` — writes a .bmp of the display area, or of the whole  |

## C-223: `save-missing-filename-arg` — 1 site · Debug Window

- **The defect:** SAVE saves the current window image to a .bmp file; used as `debug(`Bus SAVE)` with no filename
- **Correct (true fact):** SAVE syntax is SAVE {WINDOW} 'filename' — the 'filename' argument is required (not in optional braces); {WINDOW} is the only optional part.
- **Source proof:** Spin2 v55 line 1139: 'SAVE {WINDOW} 'filename' \| Save a bitmap file (.bmp) of either the entire window or just the display area.'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md §Clearing and saving, lines 25 | SAVE saves the current window image to a .bmp file; used as `debug(`Bus SAVE)` w → SAVE requires a filename: `debug(`Bus SAVE 'trace.bmp')` (optionally `SAVE WINDO |

## C-224: `scope-trigger-source-fabrication` — 1 site · IOSP

- **The defect:** Pin 52: Channel 0 (and trigger source)
- **Correct (true fact):** In %11010 scope mode each smart pin independently 'calculates an 8-bit ADC sample and checks for hysteretic triggering on every clock' via its own X trigger config; there is no designated single 'trigger source' channel.
- **Source proof:** Silicon Doc v35, p2-documentation.txt lines 8770-8814

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §16.5 Four-Channel Architecture, line 323 | Pin 52: Channel 0 (and trigger source) → Pin 52: Channel 0 — each of the four scope pins has its own independent hysteret |

## C-225: `sequential-instructions-claimed-simultaneous` — 1 site · DeSilva

- **The defect:** When you execute drvh #56 then drvl #57, 'Pin 56 goes high and pin 57 goes low at EXACTLY the same clock cycle. No skew, no uncertainty.'
- **Correct (true fact):** DRVH and DRVL each occupy 2 clock cycles and execute sequentially. Pin 57 is driven by the instruction that runs 2 clocks AFTER the one that drives pin 56, so the two pins change 2 clocks apart, not on the same clock cycle. (There is additionally a fixed pin-transition delay per Silicon Doc line 4972.)
- **Source proof:** v35 CSV rows 373-374 (DRVL/DRVH): cog-clocks column = '2' each; Silicon Doc line 4972 (DRVH pin-transition delay demonstration)

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Ch.8 §Timing Is Everything, line 2880 (prose | When you execute drvh #56 then drvl #57, 'Pin 56 goes high and pin 57 goes low a → Two separate DRVH/DRVL instructions change their pins two clocks apart. To make  |

## C-226: `servo-period-arithmetic` — 1 site · DeSilva

- **The defect:** waitx ##4_000_000 ' Rest of 20ms at 200MHz (following a 1.5ms high pulse), in a '1-2ms pulse every 20ms' servo loop
- **Correct (true fact):** 4_000_000 cycles at 200MHz is a FULL 20 ms, not the 'rest' of a 20 ms frame. Added to the preceding 1.5 ms high pulse, the loop period becomes ~21.5 ms, not the 20 ms the header comment ('1-2ms pulse every 20ms') promises.
- **Source proof:** Arithmetic against stated 200MHz clock: 4_000_000 / 200e6 = 20.0 ms; pulse 300_000/200e6 = 1.5 ms

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Ch.8 §Real-World Example: Servo Control, lin | waitx ##4_000_000 ' Rest of 20ms at 200MHz (following a 1.5ms high pulse), in a  → To hold a 20 ms frame with a 1.5 ms pulse, the low period should be 20ms - pulse |

## C-227: `setse-already-clears-flag` — 1 site · DeSilva

- **The defect:** RIGHT - Clear any stale event: setse1 #%001<<6 + PIN; pollse1 ' Clear if already set; ... waitse1 ' Now wait cleanly
- **Correct (true fact):** SETSEn clears its own SEn event flag when configured, so there is no stale event immediately after SETSE1; and a poll placed BEFORE the intervening work cannot clear an event that arrives DURING that work.
- **Source proof:** Silicon Doc p2-documentation.txt line 5457: 'SEn is cleared when matched SETSEn D/# is called.'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | §'Common Gotchas', RIGHT example, lines 5234 | RIGHT - Clear any stale event: setse1 #%001<<6 + PIN; pollse1 ' Clear if already → SETSE1 already clears SE1, so no stale flag can exist right after it. To prevent |

## C-228: `sinc2-sampling-vs-filtering-period` — 1 site · P2AN001

- **The defect:** In SINC2 sampling mode the period is 2^X[3:0] and cannot be freely dithered. ... if you change it, keep it a power of two.
- **Correct (true fact):** The power-of-two restriction belongs to SINC2 SAMPLING mode (%00). The builds here use SINC2 FILTERING mode (X=%01_0111, X[5:4]=01), which specifically ALLOWS non-power-of-2 periods via a WYPIN override — that is the reason the filtering mode exists.
- **Source proof:** Silicon Doc part4-smart-pins.txt L816 (period=POWER(2,X[3:0])), L919-921 ('SINC2 sampling ... only works at power-of-2 sample periods ... additional SINC2 filtering mode (%01) which allows non-power-of-2 sample periods'), L860-864 (WYPIN overrides period to arbitrary value in filtering modes)

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN001 | P2AN001.md §Pitfalls & Notes (Tip — sample p | In SINC2 sampling mode the period is 2^X[3:0] and cannot be freely dithered. ... → These builds use SINC2 *filtering* mode, in which the period is NOT restricted t |

## C-229: `single-pin-read-shift-always-zero` — 1 site · IOSP

- **The defect:** Right-shifting PINREAD(pin) by 31 extracts the meaningful bit for the diagnostic.
- **Correct (true fact):** A single-pin PINREAD returns 0 or 1 in bit 0; bits 1..31 are always 0, so `>> 31` always yields 0.
- **Source proof:** Spin2 v55 line 536 (PINREAD returns PinStates for the field, LSB-justified) and lines 385-393 (single-pin PINREAD returns just that pin's state = 0 or 1)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-e-troubleshooting | Right-shifting PINREAD(pin) by 31 extracts the meaningful bit for the diagnostic → For a single pin, use PINREAD(pin) directly (value is 0/1); do not `>> 31` — tha |

## C-230: `smart-pin-constant-mischaracterization` — 1 site · IOSP

- **The defect:** The Quick-Reference conditioning table describes P_LOGIC_A as 'Logic input, OUT feedback'.
- **Correct (true fact):** P_LOGIC_A drives the output from the OUT register (output = OUT), NOT feedback. 'Feedback' output routing is a distinct, separate mode selected by the _FB variant (P_LOGIC_A_FB). OUT-drive and feedback are mutually exclusive output modes, so 'OUT feedback' conflates the two.
- **Source proof:** Spin2 v55 text line 1456: 'P_LOGIC_A (default) \| Logic level A → IN, output OUT'; line 1457: 'P_LOGIC_A_FB \| Logic level A → IN, output feedback'.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-12-digital-input. | The Quick-Reference conditioning table describes P_LOGIC_A as 'Logic input, OUT  → P_LOGIC_A \| Logic-level input, output driven by OUT register (no feedback). The |

## C-231: `smart-pin-mode-in-raise-behavior` — 1 site · IOSP

- **The defect:** P_EVENTS_TICKS (mode %10010) with Y[2] = 1 raises IN either when the event arrives *or* after X clocks with no event ... so a single WAITSE1 covers both outcomes
- **Correct (true fact):** '%10010 AND Y[2] = Timeout on X clocks of missing A-input high/rise/edge': 'If no A-input high/rise/edge occurs within X clocks, IN is raised...'. 'If an A-input high/rise/edge does occur within X clocks, a new timeout period of X clocks begins and Z is reset to $00000001.' — an arriving event only resets the timer/Z; IN is NOT raised on the event, only on the timeout.
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 8134-8140 (mode %10010 AND Y[2])

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-05-working-with-smart-pins.md §5.1 ' | P_EVENTS_TICKS (mode %10010) with Y[2] = 1 raises IN either when the event arriv → In P_EVENTS_TICKS with Y[2]=1 (the timeout submode), IN is raised only when NO A |

## C-232: `smartpin-in-semantic-inaccuracy` — 1 site · DeSilva

- **The defect:** For counter modes, IN high means 'threshold reached'
- **Correct (true fact):** The P2 counting/measurement smart-pin modes raise IN at the end of each measurement PERIOD (period elapsed), not upon reaching a count threshold
- **Source proof:** Silicon Doc v35 (p2-documentation.txt, counting modes %01100-%01111): 'At the end of each period, IN will be raised and RDPIN/RQPIN can be used to retrieve the... measurement'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch14 'Understanding | For counter modes, IN high means 'threshold reached' → For counter/measurement modes, IN high = the measurement period completed (resul |

## C-233: `smartpin-missing-acknowledge` — 1 site · IOSP

- **The defect:** Example 4's watchdog loop polls PINREAD (the IN flag) to detect a timeout and later recovers ('Communication restored') when PINREAD reads false, without ever calling RDPIN/AKPIN in the timeout path.
- **Correct (true fact):** IN, once raised by a timeout, stays high until the cog acknowledges (WRPIN/WXPIN/WYPIN/RDPIN/AKPIN). Nothing in the loop acknowledges, so after the first timeout PINREAD(RX_PIN) reports true forever; comm_ok never returns to true and 'Communication restored' is unreachable.
- **Source proof:** Silicon Doc v35 part4-smart-pins.txt lines 151-153: 'A cog acknowledges a smart pin whenever it does a WRPIN, WXPIN, WYPIN, RDPIN or AKPIN on it. This causes the smart pin to lower its IN signal.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-13-timing-measurement.md §13.7 Examp | Example 4's watchdog loop polls PINREAD (the IN flag) to detect a timeout and la → Acknowledge the smart pin in the timeout branch (e.g. read RDPIN(RX_PIN) or AKPI |

## C-234: `smartpin-missing-oe` — 1 site · DeSilva

- **The defect:** UART TX configured with wrpin ##P_ASYNC_TX (no P_OE), then dirh, becomes a fully autonomous UART transmitter that sends bytes
- **Correct (true fact):** The pin's output driver is enabled by the %TT (P_OE) bits, not by the async-TX mode itself; without P_OE the pin will not drive its output
- **Source proof:** Silicon Doc v35 (part4-smart-pins.txt ~L163): '%TT bits will govern the pin's output enable, regardless of DIR state'; spin2-v55 L1525 P_OE='Enable output in smart pin mode'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch14 'The Hook: A U | UART TX configured with wrpin ##P_ASYNC_TX (no P_OE), then dirh, becomes a fully → wrpin ##P_ASYNC_TX \| P_OE, #TX_PIN — P_OE is required for the pin to actually d |

## C-235: `smartpin-register-mapping-error` — 1 site · IOSP

- **The defect:** In repository mode the value-to-store register is 'Y via WXPIN'; X[15:0] is 'Not used'.
- **Correct (true fact):** WXPIN writes the smart pin's X register; the repository long is written by WXPIN, hence it lives in X (full 32 bits), not Y.
- **Source proof:** v35 CSV row 218 WXPIN: 'Set "X" of smart pins S[10:6]+S[5:0] to D'; Silicon Doc part4-smart-pins.txt L224 '...long repository, where WXPIN writes the long...'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-f-mode-reference.md, Mode %00001 Re | In repository mode the value-to-store register is 'Y via WXPIN'; X[15:0] is 'Not → The repository long is written to X via WXPIN (X holds the 32-bit value); the ro |

## C-236: `smartpin-register-usage-omission` — 1 site · IOSP

- **The defect:** In DAC-noise sub-mode, Z (via RDPIN) is 'Not used'.
- **Correct (true fact):** In DAC-noise mode the smart pin's Z result carries the 16-bit ADC accumulation, retrievable via RDPIN/RQPIN — i.e. Z is used.
- **Source proof:** Silicon Doc part4-smart-pins.txt L246 (%00001 DAC noise): 'RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation from the last sample period.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | appendix-f-mode-reference.md, Mode %00001 Re | In DAC-noise sub-mode, Z (via RDPIN) is 'Not used'. → For DAC noise, Z via RDPIN = 16-bit ADC accumulation from the last sample period |

## C-237: `smartpin-tx-first-byte-poll` — 1 site · DeSilva

- **The defect:** The TX send routine waits (testp/if_nc jmp) for IN before every wypin, including the first byte
- **Correct (true fact):** For async-TX, IN is only raised after a word advances from buffer to shifter (i.e. after the first WYPIN); on fresh enable IN is not raised, so waiting for IN before the first WYPIN never completes
- **Source proof:** Silicon Doc v35 (p2-documentation.txt L9094-9096): async-TX state seq — during reset IN is low; 'Any time a word is advanced from the buffer to the shifter, IN is raised'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch14 'Asynchronous  | The TX send routine waits (testp/if_nc jmp) for IN before every wypin, including → Send the first byte unconditionally after enable (buffer is empty); poll IN only |

## C-238: `smartpin-wypin-reset-behavior` — 1 site · DeSilva

- **The defect:** For the trigger and serial modes the Y value is held at zero during reset, so a wypin written before dirh is simply lost
- **Correct (true fact):** The canonical configuration order is to write WRPIN/WXPIN/WYPIN while DIR is low (in reset), THEN raise DIR; WYPIN during reset establishes parameters — it is not described as 'held at zero' or 'lost'
- **Source proof:** Silicon Doc v35 (part4-smart-pins.txt ~L163): 'A smart pin should be configured while its DIR bit is low... During that time, WRPIN/WXPIN/WYPIN can be used to establish the mode and related parameters. Once configured, DIR can be raised high.'

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | COMPLETE-OPUS-MASTER.md §Ch14 'The Universal | For the trigger and serial modes the Y value is held at zero during reset, so a  → The silicon doc recommends setting all parameters (including WYPIN) while DIR is |

## C-239: `span-scope-overgeneralization` — 1 site · IOSP

- **The defect:** Smart pin instructions operate on a span of pins exactly as the Direct I/O instructions do (§1.9), with the span in the S operand.
- **Correct (true fact):** Only WRPIN, WXPIN, WYPIN, and AKPIN support pin spans. RDPIN and RQPIN — which §4.1 of this very chapter lists as 'smart pin instructions' — are NOT span-capable (they read a single pin's result into one D register).
- **Source proof:** Silicon Doc p2-documentation.txt L91-92 'WRPIN/WXPIN/WYPIN/AKPIN can now work on a span of pins (+S[10:6] pins). Prior SETQ overrides S[10:6].'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-04-smart-pin-configuration.md §4.11, | Smart pin instructions operate on a span of pins exactly as the Direct I/O instr → The write/acknowledge smart pin instructions (WRPIN, WXPIN, WYPIN, AKPIN) operat |

## C-240: `sparse-round-pixels-vs-square-block` — 1 site · Debug Window

- **The defect:** DOTSIZE with SPARSE draws each logical pixel as a DOTSIZE-square block with a grid border.
- **Correct (true fact):** SPARSE renders each magnified pixel as a large ROUND pixel (dot) against the (border) background color — not a filled square block. Plain DOTSIZE without SPARSE gives the square magnified block.
- **Source proof:** Spin2 v55 text: 'SPARSE color \| Show large round pixels against a colored background' (BITMAP Instantiation) + v37 changelog 'plot large round pixels against a background color'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch04-bitmap.md §Considerations, line 400 (si | DOTSIZE with SPARSE draws each logical pixel as a DOTSIZE-square block with a gr → With SPARSE the window draws each magnified pixel as a large round dot on the SP |

## C-241: `spi-clock-data-rate-mismatch` — 1 site · Streamer

- **The defect:** Clock pin: wxpin ##2 (transition base period = 2 clocks) paired with NCO setxfrq ##$4000_0000 ('NCO at half clock rate'), then wypin #16 for 8 data bits.
- **Correct (true fact):** In transition mode each transition occurs once per base period; base period 2 makes each clock half-period 2 sysclks, so a full SPI clock cycle = 4 sysclks. But the streamer at NCO ÷2 emits one data bit every 2 sysclks, so 16 transitions span 32 sysclks while the 8 data bits span only 16 sysclks — the clock runs at half the data rate.
- **Source proof:** Silicon Doc part4-smart-pins.txt L351-359 (transition mode %00101: 'X[15:0] establishes a base period... high-time and low-time units... pin toggles for Y transitions at each base period'); NCO 1:2 ratio = $4000_0000 (doc §3.2 table, silicon-consistent) → 2 sysclks per data element.

| Document | Location | before → after |
|----------|----------|----------------|
| Streamer | streamer-body.md §16.1 SPI Output, lines 123 | Clock pin: wxpin ##2 (transition base period = 2 clocks) paired with NCO setxfrq → For 1 clock pulse per bit aligned with NCO ÷2 data, use base period 1 (wxpin ##1 |

## C-242: `spin2-cordic-method-name-wrong` — 1 site · Debug Window

- **The defect:** the CORDIC solver — `QSIN` / `QROTATE` for smooth waveforms and rotations
- **Correct (true fact):** Spin2's CORDIC rotation built-in method is `ROTXY` (also `POLXY`/`XYPOL`). `QSIN` is a real Spin2 method, but `QROTATE` is a PASM2 instruction, not a Spin2 built-in method.
- **Source proof:** Spin2 v55 line 561: `ROTXY(x, y, angle32bit) : rotx, roty \| Rotate (x,y) by angle32bit`; line 564: `QSIN(length, step, stepsInCircle) : y`; no `QROTATE` Spin2 method exists (QROTATE is a PASM2 instruction)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch02-getting-started.md §The no-hardware phi | the CORDIC solver — `QSIN` / `QROTATE` for smooth waveforms and rotations → the CORDIC solver — `QSIN` / `ROTXY` for smooth waveforms and rotations |

## C-243: `spin2-method-existence-error` — 1 site · IOSP

- **The defect:** There is no direct Spin2 equivalent [to AKPIN]. Use RDPIN with a discard variable to acknowledge.
- **Correct (true fact):** Spin2 provides a built-in AKPIN(PinField) method that acknowledges a smart pin without reading Z — a direct equivalent of the PASM2 AKPIN instruction.
- **Source proof:** Spin2 v55 ref line 542: "AKPIN(PinField) \| Acknowledge PinField smart pin(s)."

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-04-smart-pin-configuration.md §4.7 A | There is no direct Spin2 equivalent [to AKPIN]. Use RDPIN with a discard variabl → Spin2 provides AKPIN(PinField), the direct equivalent of the PASM2 AKPIN instruc |

## C-244: `spin2-method-pasm-equivalent-incomplete` — 1 site · IOSP

- **The defect:** PINCLEAR Equivalent PASM2: WRPIN #0, pin
- **Correct (true fact):** PINCLEAR performs DIR=0 (DIRL) AND WRPIN=0; WRPIN #0 alone does not reproduce the DIR=0 (float) step.
- **Source proof:** Spin2 v55 text line 538: 'PINCLEAR(PinField) \| Clear PinField smart pin(s): DIR=0, then WRPIN=0.'

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §1.8 PINCLEAR, line 1099 | PINCLEAR Equivalent PASM2: WRPIN #0, pin → Equivalent PASM2: DIRL pin followed by WRPIN #0, pin (PINCLEAR sets DIR=0 and cl |

## C-245: `spin2-rev-operand-off-by-one` — 1 site · IOSP

- **The defect:** value := value REV 32  ' Reverse all 32 bits (then value := value & $FF)
- **Correct (true fact):** Spin2 'x REV y' reverses bits 0..y (i.e. the low y+1 bits) and zero-extends. To reverse all 32 bits the operand must be 31. The compiler masks the operand to 5 bits, so REV 32 == REV 0, which keeps only bit 0 and clears the rest: $FF000000 REV 32 folds to $00000000 (verified), whereas $FF000000 REV 31 correctly folds to $000000FF.
- **Source proof:** Spin2 v55 spin2-v55-text.txt line 448 ('\| REV \| x REV y \| ... \| Reverse order of bits 0..y of x and zero-extend \|'); pnut-ts v1.55.0 constant-fold: $FF000000 REV 32 = $00000000, $FF000000 REV 31 = $000000FF

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §17.3 MSB-First Reception, line 229 | value := value REV 32  ' Reverse all 32 bits (then value := value & $FF) → value := value REV 31  ' Reverse all 32 bits — REV 31 (not 32) reverses bits 0.. |

## C-246: `sprite-version-gating-wrong` — 1 site · Debug Window

- **The defect:** {Spin2_v50} required. LAYER, CROP, SPRITEDEF, and SPRITE are V50 additions.
- **Correct (true fact):** Sprites (SPRITEDEF/SPRITE) were added in v35n (2021). The v50 changelog entry adds only the hidden bitmap LAYER and CROP capability. Only LAYER and CROP are v50 additions.
- **Source proof:** Spin2 v55 text.txt line 20 (v35n, 2021-05-23): 'Sprites added to DEBUG PLOT window'; line 42 (v50, 2025-02-16) lists only LAYER and CROP

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch05-plot.md §Layers, CROP, and sprites call | {Spin2_v50} required. LAYER, CROP, SPRITEDEF, and SPRITE are V50 additions. → LAYER and CROP are {Spin2_v50} additions. SPRITEDEF and SPRITE were added earlie |

## C-247: `stray-ellipsis-in-runnable-example` — 1 site · Debug Window

- **The defect:** the named runnable example ch06-logic-spi-bus.spin2 creates the window with `SAMPLES 200 SPACING 3 ...`
- **Correct (true fact):** The literal '...' is not Spin2 line-continuation; it is compiled into the LOGIC creation command as literal content, altering the emitted display command.
- **Source proof:** pnut-ts v1.55.0 compile: with '...' the binary is 9438 bytes; with '...' removed it is 9435 bytes (3-byte diff = the three dots embedded into the DEBUG display command stream).

TODO: it is spin2 line continuation, just not within debug() statements, possibly?

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md §A complete software-only exam | the named runnable example ch06-logic-spi-bus.spin2 creates the window with `SAM → Remove the stray '...'; the debug() call already spans two lines legally inside  |

## C-248: `table-default-value-wrong` — 1 site · Debug Window

- **The defect:** TITLE default is `Plot` (the window's title-bar text)
- **Correct (true fact):** The TITLE instantiation keyword's default is <none> (no caption string supplied).
- **Source proof:** Spin2 v55 text.txt line 1255: TITLE 'string' \| Set the window caption to 'string'. \| Default: <none>

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch05-plot.md §Creating a PLOT window table,  | TITLE default is `Plot` (the window's title-bar text) → TITLE has no default caption string (v55: <none>); the chapter's claim that the  |

## C-249: `term-default-pos` — 1 site · Debug Window

- **The defect:** The POS keyword defaults to 'auto' screen positioning.
- **Correct (true fact):** The documented default position is 0, 0 (top-left), not 'auto'.
- **Source proof:** Spin2 v55 TERM Instantiation: 'POS left top \| Set the window position. \| 0, 0' (spin2-v55-text.txt line 1123)

TODO there is a pnut-term-ts behavior that when a window is created without POS directive the window is auto-placed (maybe this led to this confusion and needs to be stated clearly?)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch03-term.md §Creating a TERM window, config | The POS keyword defaults to 'auto' screen positioning. → POS defaults to 0, 0 per the language reference (though PNut may cascade windows |

## C-250: `term-default-title` — 1 site · Debug Window

- **The defect:** The TITLE keyword's default title-bar text is `TERM`.
- **Correct (true fact):** The documented default for TITLE is <none>, not the literal string 'TERM'.
- **Source proof:** Spin2 v55 TERM Instantiation: 'TITLE \'string\' \| Set the window caption to \'string\'. \| <none>' (spin2-v55-text.txt line 1122)

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch03-term.md §Creating a TERM window, config | The TITLE keyword's default title-bar text is `TERM`. → Default title/caption is <none> (no caption set), not 'TERM'. |

## C-251: `test-vs-testb-bit-extract` — 1 site · Assembly (Part I)

- **The defect:** test data, #31 wc ' Get high bit into C flag
- **Correct (true fact):** TEST D,#S sets C to the PARITY of (D AND S). With S=#31 (=%11111), it computes parity of the low 5 bits of data — not the high bit. To place bit 31 into C you must use TESTB data,#31 WC (C = D[31]).
- **Source proof:** CSV row 81 TEST D,{#}S: 'C = parity of (D & S)'; CSV row 34 TESTB D,{#}S WC/WZ: 'C/Z = D[S[4:0]]'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.6.4 Deterministic I/ | test data, #31 wc ' Get high bit into C flag → Use `testb data, #31 wc` — TESTB tests bit S of D and writes that bit to C (C =  |

## C-252: `test-z-flag-inverted` — 1 site · Assembly (Part I)

- **The defect:** Each TEST sets Z if the state bit is set, and the conditional jump executes for that state.
- **Correct (true fact):** TEST sets Z=1 when the tested bits are CLEAR (the AND is zero); Z=0 when the state bit is set. So `test state,#STATE_IDLE wz / if_z jmp #handle_idle` jumps when the state bit is NOT set — the opposite of the stated intent.
- **Source proof:** v35 CSV row 81 (TEST): 'Test D with S. C = parity of (D & S). Z = ((D & S) == 0).'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-03-flags.md §3.6.4 line 550 (code li | Each TEST sets Z if the state bit is set, and the conditional jump executes for  → Each TEST sets Z when the state bit is CLEAR. To branch to a handler when a stat |

## C-253: `testp-both-flags-overclaim` — 1 site · IOSP

- **The defect:** TESTP/TESTPN set both C and Z to the pin's input state.
- **Correct (true fact):** TESTP/TESTPN take WC/WZ (mutually exclusive) — the pin's input state is written to C (with WC) OR Z (with WZ), never to both flags in a single instruction. There is no WCZ form.
- **Source proof:** v35 CSV rows 341-348: TESTP/TESTPN syntax '{#}D WC/WZ'; C/Z = IN[D[5:0]] (single flag)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §1.10 Instruction Quick Reference, legend, l | TESTP/TESTPN set both C and Z to the pin's input state. → TESTP/TESTPN write the pin's input state to C (with WC) or Z (with WZ) — one fla |

## C-254: `testp-flag-polarity-inverted` — 1 site · DeSilva

- **The defect:** if_z jmp #sensor_low ' Jump if pin low (Z=1 when pin=0)  /  if_nz jmp #sensor_high ' Jump if pin is high
- **Correct (true fact):** TESTP with WZ writes the pin's IN state directly into Z: Z = IN[pin]. Therefore Z=1 when the pin is HIGH (1), and Z=0 when the pin is LOW (0) — the opposite of what the comment states.
- **Source proof:** v35 CSV row 341 (TESTP {#}D WC/WZ): 'C/Z = IN[D[5:0]]'; Silicon Doc p2-documentation.txt line 5038; YAML p2kbPasm2Testp flags_affected

| Document | Location | before → after |
|----------|----------|----------------|
| DeSilva | Ch.8 §Reading Multiple Pins area, line 2664  | if_z jmp #sensor_low ' Jump if pin low (Z=1 when pin=0)  /  if_nz jmp #sensor_hi → testp #SENSOR_PIN wz sets Z to the pin state, so Z=1 when the pin is HIGH. if_z  |

## C-255: `testp-wz-flag-polarity-inverted` — 1 site · IOSP

- **The defect:** After `testp #pin wz`, `if_z jmp #pin_low ' Branch if zero (low)` — treats Z=1 as pin low.
- **Correct (true fact):** TESTP writes the pin's IN bit directly into Z. Z = IN[pin], so Z=1 means the pin is HIGH (1), not low.
- **Source proof:** v35 CSV row 341 (TESTP): "Test IN bit of pin D[5:0], write to C/Z. C/Z = IN[D[5:0]]."; Silicon Doc p2-documentation.txt:4968 "read pin D bit in INx and affect C or Z"

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-3-input-modes/chapter-12-digital-input. | After `testp #pin wz`, `if_z jmp #pin_low ' Branch if zero (low)` — treats Z=1 a → `testp #pin wz` sets Z = pin state; Z=1 means the pin is HIGH. The branch should |

## C-256: `textstyle-default-value-wrong` — 1 site · Debug Window

- **The defect:** The defaults (style $00) are light weight, centered both ways.
- **Correct (true fact):** The default TEXTSTYLE is %00000001 ($01): weight %01 = normal, centered both ways. Not $00 (light weight).
- **Source proof:** Spin2 v55 text.txt line 1282: TEXTSTYLE ... Default: %00000001

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch05-plot.md §TEXT / style byte, line 314 | The defaults (style $00) are light weight, centered both ways. → The default text style is $01 (%00000001): NORMAL weight, centered both horizont |

## C-257: `title-recipe-technique-mismatch` — 1 site · P2AN004

- **The defect:** Title: "...by Frequency, Period, and RC Timing on a P2 Pin" naming three techniques (Frequency, Period, RC Timing), while the box lists three recipes R1 RC-decay, R2 light-to-frequency, R3 quadrature-knob.
- **Correct (true fact):** Quadrature encoder mode counts A/B phase steps (position/count), which is neither frequency nor period measurement; there is no recipe on this cover corresponding to the title's "Period" technique.
- **Source proof:** Silicon Doc part4-smart-pins.txt: %01011 A/B quadrature encoder (line 531); time-measurement %10000/%10001 (lines 649,669); edge-count %01100/%01110 (lines 558,601)

| Document | Location | before → after |
|----------|----------|----------------|
| P2AN004 | front-matter.md §title vs What-You'll-Build  | Title: "...by Frequency, Period, and RC Timing on a P2 Pin" naming three techniq → Title's three named techniques should match the three recipes: Frequency (R2), R |

## C-258: `two-clocks-per-instruction-overgeneralization` — 1 site · Getting Started

- **The defect:** PASM2 is native assembly: it runs at the deterministic two-clocks-per-instruction speed from Chapter 1, with cycle-exact timing
- **Correct (true fact):** Two clocks is the MINIMUM per instruction, not a universal rate: instructions that stall take more, taken branches flush the pipeline (extra clocks), and hub reads/writes are variable (RDLONG 9..16 cog clocks). Not every PASM2 instruction runs in exactly two clocks.
- **Source proof:** Silicon Doc p2-documentation.txt:629-631 ('takes as little as two clock cycles to execute. If an instruction stalls for additional clock cycles...'; 'Branch instructions cause the pipeline to be flushed'); hub-read instrs are variable (RDLONG 9..16 clocks)

| Document | Location | before → after |
|----------|----------|----------------|
| Getting Started | getting-started-body.md Ch3 §"Spin2 or PASM2 | PASM2 is native assembly: it runs at the deterministic two-clocks-per-instructio → PASM2 register-to-register instructions typically execute in two clocks; branche |

## C-259: `vco-out-of-range-example` — 1 site · Assembly (Part I)

- **The defect:** 20 MHz crystal, divider 1, multiplier 16, post divider 2 -> 160 MHz; the VCO operates optimally between 100-200 MHz.
- **Correct (true fact):** VCO = f_ref × (M+1)/(D+1) = 20 MHz × 16 = 320 MHz for the doc's example — well outside the 100-200 MHz range the doc states two sentences later. Silicon's own example deliberately keeps VCO at 148.5 MHz.
- **Source proof:** Silicon Doc v35 lines ~6100 & 6240 (PLL Example): 'VCO should be kept within 100 MHz to 200 MHz'; worked example VCO=148.5 MHz

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.1.2 PLL example vs V | 20 MHz crystal, divider 1, multiplier 16, post divider 2 -> 160 MHz; the VCO ope → Pick example parameters whose implied VCO (f_ref × multiplier / input_div) lands |

## C-260: `version-gating-wrong` — 1 site · Debug Window

- **The defect:** The LAYER, CROP, and sprite commands are V50 additions.
- **Correct (true fact):** LAYER and CROP were added in v50, but the SPRITE/SPRITEDEF (sprite) commands were added much earlier, in v35n (2021-05-23) — they are NOT v50 additions.
- **Source proof:** Spin2 v55 changelog: v35n (2021-05-23) 'Sprites added to DEBUG PLOT window'; v50 (2025-02-16) 'Hidden bitmap layers are now loadable... LAYER/CROP'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch15-panels.md §Technique 3 callout, line 10 | The LAYER, CROP, and sprite commands are V50 additions. → LAYER and CROP are V50 additions; the SPRITE/SPRITEDEF commands were added earli |

## C-261: `vga-vertical-porch-swap` — 1 site · Streamer

- **The defect:** vertical front porch = 10 lines placed after vsync (frame start, before visible); vertical back porch = 33 lines placed after visible (before vsync)
- **Correct (true fact):** Front porch is the blanking immediately BEFORE the sync pulse (after visible) = 10 lines; back porch is the blanking immediately AFTER the sync pulse (before visible) = 33 lines. The silicon example puts the post-sync blank before visible and the pre-sync blank after visible.
- **Source proof:** Silicon Doc HDMI example p2-documentation.txt lines 4551/4572 (post-sync 'top blanks' then visible then pre-sync 'bottom blanks'); VESA 640x480@60 standard vertical timing

| Document | Location | before → after |
|----------|----------|----------------|
| Streamer | streamer-body.md §15.1 VGA Output, lines 112 | vertical front porch = 10 lines placed after vsync (frame start, before visible) → Place the 10-line front porch AFTER the visible lines (immediately before the vs |

## C-262: `vga-visible-dac-routing-missing` — 1 site · Streamer

- **The defect:** m_visible long $B085_0000 + 640  (= X_RFWORD_RGB16 \| X_PINS_ON, DAC-routing field %dddd = %0000)
- **Correct (true fact):** For streamer data to appear on the DAC channels the %dddd field (D[27:24]) must route the streamer's X3/X2/X1 channels; %dddd=%0000 (X_DACS_OFF) means no override, so the static SETDACS values output during visible pixels, not the RGB data.
- **Source proof:** Silicon Doc v35 §DAC-routing D[27:24] table (p2-documentation.txt L3525-3527, L4757 'DAC3/DAC2/DAC1 serve as R/G/B channels'); command-word decode: $B085_0000 → mode=%1011, %dddd=%0000 (X_DACS_OFF), D[23]=1 (pins on)

| Document | Location | before → after |
|----------|----------|----------------|
| Streamer | streamer-body.md §15.1 VGA Output, line 1161 | m_visible long $B085_0000 + 640  (= X_RFWORD_RGB16 \| X_PINS_ON, DAC-routing fie → The visible-line command must route the RGB data to the DAC channels, e.g. m_vis |

## C-263: `waitatn-pin-transition-fabrication` — 1 site · Assembly (Part I)

- **The defect:** WAITATN waits for any pin to make a low-to-high transition (attention flag). Smart pins can be configured to set their ATN flags on specific conditions, making WAITATN useful for waiting on external events
- **Correct (true fact):** COGATN 'strobes attention of all cogs whose corresponding bits are high in D[15:0]'; WAITATN 'Wait for ATN event flag'. Event 14 = 'Attention was requested by another cog or other cogs.' ATN is an inter-cog attention strobe, not a pin transition.
- **Source proof:** Silicon Doc v35 lines 5070-5109, 5144 (COG ATTENTION); CSV row 301 WAITATN, row 340 COGATN

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.5.3 Pin-Based Synchr | WAITATN waits for any pin to make a low-to-high transition (attention flag). Sma → WAITATN waits for the ATN (attention) event, which another cog raises via COGATN |

## C-264: `waitx-plus2-overhead` — 1 site · Assembly (Part I)

- **The defect:** waitx ##100 ' Wait exactly 100 cycles ... Execution resumes exactly after that many cycles have elapsed
- **Correct (true fact):** WAITX consumes 2 + D clocks. `waitx ##100` therefore occupies 102 clocks, not exactly 100.
- **Source proof:** CSV row 266 WAITX {#}D {WC/WZ/WCZ}: 'Wait 2 + D clocks if no WC/WZ/WCZ.'

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-04-timing.md §4.5.1 WAITX, lines 379 | waitx ##100 ' Wait exactly 100 cycles ... Execution resumes exactly after that m → `waitx ##100` occupies 2 + 100 = 102 clocks. For a delay of exactly N clocks the |

## C-265: `windowed-mode-minimum-vs-fixed-clocks` — 1 site · IOSP

- **The defect:** The windowed measurement modes (%10101-%10111, Chapter 15) instead raise IN after a fixed number of clocks, giving a "wait exactly this long, then read" cadence.
- **Correct (true fact):** 'X[31:0] establishes the MINIMUM number of clock cycles to track periods for.' and 'A measurement is taken across some number of A-input rise/edge to B-input rise/edge periods, until X clock cycles elapse AND THEN any period in progress completes. ... Upon completion, the measurement is placed in Z, IN is raised.' — IN is raised after AT LEAST X clocks plus the tail of the in-progress period, a va
- **Source proof:** Silicon Doc v35 p2-documentation.txt lines 8165-8182 (modes %10101-%10111)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-05-working-with-smart-pins.md §5.1 ' | The windowed measurement modes (%10101-%10111, Chapter 15) instead raise IN afte → The windowed modes (%10101-%10111) treat X as a MINIMUM window: they accumulate  |

## C-266: `worked-example-bit-mapping-error` — 1 site · Debug Window

- **The defect:** a sample value of %1011 lights channel 0 (CLK) high, channel 1 (DATA) low, channel 2 (CS) high, channel 3 (WR) high
- **Correct (true fact):** Data is applied LSB-first: channel 0 = bit0, channel 1 = bit1, etc. %1011 = bit0=1,bit1=1,bit2=0,bit3=1.
- **Source proof:** Spin2 v55 line 1137: 'data \| Numerical data is applied LSB-first to the channels.'

| Document | Location | before → after |
|----------|----------|----------------|
| Debug Window | ch06-logic.md §Creating a LOGIC window, conf | a sample value of %1011 lights channel 0 (CLK) high, channel 1 (DATA) low, chann → %1011 lights channel 0 (CLK) high, channel 1 (DATA) HIGH, channel 2 (CS) LOW, ch |

## C-267: `worked-example-init-logic-bug` — 1 site · IOSP

- **The defect:** The sweep starts at 1 kHz (setup 'wypin y_start' / y_start=21475) and sweeps upward to 10 kHz.
- **Correct (true fact):** y_current begins at 0 and the loop's first WYPIN writes 215 (~10 Hz), overwriting the y_start=21475 (1 kHz) set during setup. The sweep therefore starts near 10 Hz, not 1 kHz.
- **Source proof:** Code trace: y_current initialized 'long 0' (line 408); loop first executes 'add y_current, y_step' (y_current=215) then 'wypin y_current' before any use of y_start after setup

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-2-output-modes/chapter-08-nco-frequency | The sweep starts at 1 kHz (setup 'wypin y_start' / y_start=21475) and sweeps upw → Initialize y_current := y_start (or seed y_current long 21475) so the sweep actu |

## C-268: `worked-example-logic-error` — 1 site · IOSP

- **The defect:** The triangle-wave loop reverses direction when value16 reaches $FFFF (top) or 0 (bottom), producing a triangle wave.
- **Correct (true fact):** With a step of 256, value16 skips 65535 entirely (65280 -> 65536), so 'cmp value16, ##$FFFF wz' never matches and direction never reverses at the top; value16 keeps growing (WYPIN uses only Y[15:0], so the pin wraps as a sawtooth), not the claimed triangle.
- **Source proof:** Logic/arithmetic analysis: value16 starts 0 and is incremented by direction=256 each iteration (0,256,...,65280,65536,...), so it is never exactly $FFFF (65535); the CMP ... wz equality test therefore never sets Z at the top of the ramp.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | chapter-10-dac-output.md §10.8 Example 4 (PA | The triangle-wave loop reverses direction when value16 reaches $FFFF (top) or 0  → To bound a triangle whose step is 256, test the boundary with a range/comparison |

## C-269: `wrlut-clock-comparison` — 1 site · Assembly (Part I)

- **The defect:** 'RDLUT takes 3 clock cycles and WRLUT takes 2 cycles—both faster than hub access but slower than direct cog register operations.'
- **Correct (true fact):** WRLUT is 2 clocks — the SAME as a direct cog-register operation (2 clocks), not slower. Only RDLUT (3 clocks) is slower than a cog-register op.
- **Source proof:** v35 CSV row 220 (WRLUT) = 2 clocks; row 151 (RDLUT) = 3 clocks; a standard cog-register ALU op (e.g. MOV/ADD) = 2 clocks (Silicon Doc line 628-629, 'as little as two clock cycles').

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-01-execution-model.md §1.3.1 line 91 | 'RDLUT takes 3 clock cycles and WRLUT takes 2 cycles—both faster than hub access → RDLUT (3 clocks) is slower than a direct cog-register operation, while WRLUT (2  |

## C-270: `wrpin-mode-field-bit-position` — 1 site · IOSP

- **The defect:** mode bits \| Bits [4:0] in WRPIN value selecting Smart Pin mode
- **Correct (true fact):** The 5-bit smart-pin mode selector (%SSSSS) occupies WRPIN D-operand bits [5:1]; bit [0] is a separate trailing bit, not part of the mode field.
- **Source proof:** Silicon Doc part4-smart-pins.txt line 212 ('set by the %SSSSS bits within the D[5:1] operand of the WRPIN instruction') and layout line 10: %AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | front-matter.md, Document Conventions > Term | mode bits \| Bits [4:0] in WRPIN value selecting Smart Pin mode → mode bits \| Bits [5:1] in the WRPIN D value selecting Smart Pin mode (%SSSSS);  |

## C-271: `x-zero-continuous-overgeneralization` — 1 site · IOSP

- **The defect:** Setting X=0 universally means continuous operation with no IN flag; X>0 means periodic with IN raised each period.
- **Correct (true fact):** The meaning of X=0 is mode-specific: for ADC sample/filter modes X[3:0]=0 gives a 1-clock period; for DAC/scope modes X[15:0]=0 means 65,536 clocks — not a universal 'continuous, no IN flag'.
- **Source proof:** Silicon Doc part4-smart-pins.txt line 242 (DAC modes: X[15:0]=0 → 65,536 clocks) and line 816 (ADC modes: sample period = POWER(2, X[3:0]), so X[3:0]=0 → 1 clock)

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | part-5-appendices/appendix-e-troubleshooting | Setting X=0 universally means continuous operation with no IN flag; X>0 means pe → Whether X=0 means 'continuous' depends on the smart pin mode; for ADC and DAC mo |

## C-272: `xbyte-overhead-clock-accounting` — 1 site · Assembly (Part I)

- **The defect:** Total XBYTE dispatch overhead is 6 clock cycles, yet the Dispatch Cycle table lists dispatch activity across clocks 1-7 with the handler's first instruction not until clock 8.
- **Correct (true fact):** Silicon: overhead is 6 clocks EXCLUDING the routine; clock 1 is 'Last clock of the RET/_RET_ to $1FF' (it overlaps the triggering RET), clock 8 is the handler's first instruction — so the 6 overhead clocks are clocks 2-7, and the full loop is 8 clocks.
- **Source proof:** Silicon Doc p2-documentation.txt lines 1966-1969 ('total overhead of only 6 clocks, excluding the bytecode routine ... total XBYTE loop take only 8 clocks') and clock table lines 1984-2058

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.6 / §5.6.1 XBYTE,  | Total XBYTE dispatch overhead is 6 clock cycles, yet the Dispatch Cycle table li → State that clock 1 overlaps the triggering RET (so it is not counted in overhead |

## C-273: `xcont-used-to-start-streamer` — 1 site · Streamer

- **The defect:** The RGB16 video-output example starts the streamer with 'xcont cmd, #0' as its sole/first streamer command (after rdfast + setxfrq), with no preceding XINIT.
- **Correct (true fact):** XCONT is for seamless command-to-command continuity and does not clear the phase accumulator; if the streamer is idle it runs immediately with whatever phase remains. XINIT is what (re)starts the streamer from a zeroed phase. The document's own §4.7 caution states: 'XCONT and XZERO are for seamless command-to-command continuity, not for starting the streamer... XCONT begins with whatever phase rem
- **Source proof:** Silicon Doc v35 lines 3506-3519 (XINIT (re)starts the streamer; XZERO/XCONT wait for the prior command's last clock, but 'If the streamer count has already run down to 0, there is no waiting'; XCONT does not affect the phase accumulator). Doc's own §4.7 caution, lines 360-362.

| Document | Location | before → after |
|----------|----------|----------------|
| Streamer | streamer-body.md §7.3 RGB Mode Example, line | The RGB16 video-output example starts the streamer with 'xcont cmd, #0' as its s → If this snippet is the first streamer command (starting output from idle), it sh |

## C-274: `xro-nco-rollover-not-circular-buffer` — 1 site · Assembly (Part I)

- **The defect:** XRO \| Streamer rollover \| Circular buffer management
- **Correct (true fact):** Event 12 / XRO = 'Streamer NCO rollover occurred' — the streamer's numerically-controlled-oscillator (DDS phase accumulator) rolling over, a signal-timing event, not a memory circular-buffer boundary.
- **Source proof:** Silicon Doc p2-documentation.txt line 5142 (Event 12) + line 5513

| Document | Location | before → after |
|----------|----------|----------------|
| Assembly (Part I) | chapter-05-hardware.md §5.4.1 line 351 (even | XRO \| Streamer rollover \| Circular buffer management → XRO = streamer NCO rollover (the DDS phase accumulator overflowing), used for wa |

## C-275: `z-cap-inconsistent-across-mode-tables` — 1 site · IOSP

- **The defect:** Z register descriptions for %10011/%10101/%10110 (no max stated) vs %10100/%10111 (stated max $80000000).
- **Correct (true fact):** Silicon caps Z at $80000000 for all five modes in this chapter, yet the doc states the cap only for %10100 (line 111) and %10111 (line 221), omitting it for %10011 (line 79), %10101 (line 163), and %10110 (line 196).
- **Source proof:** Silicon Doc part4-smart-pins.txt line 749 and line 786: 'Z will be limited to $80000000' — applies to BOTH the %10011/%10100 group and the %10101/%10110/%10111 group.

| Document | Location | before → after |
|----------|----------|----------------|
| IOSP | §15.2 P_PERIODS_TICKS registers table, line  | Z register descriptions for %10011/%10101/%10110 (no max stated) vs %10100/%1011 → State 'max $80000000' consistently in the Z row of every mode's register table ( |

---

## Extra same-class instances swept (17) — additional occurrences the editors caught beyond the enumerated findings

| Document | Location | Class | before → after | Source |
|----------|----------|-------|----------------|--------|
| DeSilva | Ch12 L4064 (within #40/#41 FIFO bloc | cycle-count-vs-instruc | ' 3x faster for sequential reads! → ' ~2x faster for sequential reads! | v35 CSV: traditional loop ~13-19 clocks vs FIFO lo |
| DeSilva | Ch1 L257 CORDIC teaser | cordic-fixed-latency-o | with results ready in exactly 55 clocks. Eve → with results ready about 55 clocks after the | Silicon Doc p2-documentation.txt:7290-7291 (0 to c |
| DeSilva | Ch7 L2174 Hook prose | cordic-per-cog-fabrica | a dedicated trigonometric coprocessor sittin → a hardware trigonometric coprocessor—a singl | Silicon Doc p2-documentation.txt:7271 (one 54-stag |
| DeSilva | Appendix L5902 comparison table | cordic-fixed-latency-o | Hardware trig in exactly 55 clocks → Hardware trig in ~55 clocks | Silicon Doc p2-documentation.txt:7290-7291 |
| DeSilva | Index L6098 | q-register-mislabeled- | - Q flag: Ch7 → - Q register: Ch7 | Silicon Doc p2-documentation.txt:2522 'SETQ/SETQ2  |
| DeSilva | Ch14 L4844 and L4852 (DIRH-ordering  | smartpin-missing-oe | wrpin ##P_ASYNC_TX, #PIN → wrpin ##P_ASYNC_TX \| P_OE, #PIN | Spin2 v55 L1525 P_OE 'Enable output in smart pin m |
| Debug Window | ch05-plot.md §Color and opacity, lin | table-default-value-wr | accepted in the command stream. Until you se → accepted in the command stream. Until you se | Spin2 v55 text.txt line 1268 (PLOT Feeding): 'COLO |
| IOSP | §9.3 Configuration Sequence, sawtoot | frame-field-16bit-over | PUB sawtooth_pwm(freq_hz, duty_percent) \| f → PUB sawtooth_pwm(freq_hz, duty_percent) \| b | Silicon Doc part4-smart-pins.txt: frame period is  |
| IOSP | §11.3 SPI Master PASM2 example, line | clock-halfperiod-label | wxpin     ##$1000, #CLK_PIN     ' Clock peri → wxpin     ##$1000, #CLK_PIN     ' Clock half | Silicon Doc p2-documentation.txt lines 7961-7962 ( |
| IOSP | §12.9 Example 1 line 410 | pinfloat-disables-inte | WRPIN(BUTTON_PIN, P_SCHMITT_A \| P_HIGH_15K) → WRPIN(BUTTON_PIN, P_SCHMITT_A \| P_HIGH_15K) | Spin2 v55:1506; Silicon:7640-7641; Spin2 v55:535 P |
| IOSP | §12.9 Example 2 line 431 | pinfloat-disables-inte | WRPIN(BUTTON_BASE + i, P_SCHMITT_A \| P_HIGH → WRPIN(BUTTON_BASE + i, P_SCHMITT_A \| P_HIGH | Spin2 v55:1506; Silicon:7640-7641; Spin2 v55:535 P |
| IOSP | §12.9 Example 3 line 467 (PASM2 dirl | pinfloat-disables-inte | dirl      pin                 ' Input mode → drvh      pin                 ' DIR=1, OUT=1 | Silicon:7640-7641 (smart-pin off: DIR enables outp |
| IOSP | §15.6 Example 3 (PWM Analyzer), line | neighbor-pin-input-rou | PINSTART(PWM_PIN, P_PERIODS_TICKS, NUM_PERIO → PINSTART(PWM_PIN, P_PERIODS_TICKS, NUM_PERIO | Same as §15.2 findings: part4-smart-pins.txt %AAAA |
| IOSP | §15.9 Quick Reference frequency form | frequency-counter-exac | ' Or for 1-second window: frequency = rdpin_ → ' Or for a ~1-second window (window runs sli | part4-smart-pins.txt: window is a minimum that ove |
| IOSP | §16.3 SINC2 Filtering Mode config ex | gio-reference-used-as- | WRPIN(ADC_PIN, P_ADC_GIO \| P_ADC) → WRPIN(ADC_PIN, P_ADC_1X \| P_ADC) | spin2-v55-text.txt line 1466/1469; this doc §16.2  |
| IOSP | §16.3 Bitstream Capture Mode config  | gio-reference-used-as- | WRPIN(ADC_PIN, P_ADC_GIO \| P_ADC) → WRPIN(ADC_PIN, P_ADC_1X \| P_ADC) | spin2-v55-text.txt line 1466/1469; this doc §16.2  |
| IOSP | §Debugging Techniques / Using RDPIN  | rdpin-c-in-bit31-unmas | ' Read without clearing IN z_value := RQPIN( → ' Read without clearing IN (bit 31 is the RQ | Spin2 v55 spin2-v55-text.txt L544: 'RQPIN(Pin) : Z |

---

## Genuine skips (2) — NOT changed (need your call / out of scope)

- **Debug Window — ch05-plot.md §Creating a PLOT window table, line 41 (POS default 'auto')** (`table-default-value-wrong`): not flagged and genuinely ambiguous — v55 line 1256 lists POS default literally as '0, 0', but PNut auto-places/cascades windows when POS is omitted, so 'auto' may be the reader-correct description. No confident Tier-1 basis to change 'auto' to '0,0'; left unt
- **IOSP — §12.3 line 99 (P_LOGIC_B_FB example comment)** (`smart-pin-constant-mischaracterization`): Not a listed finding; the finding-9 verifier explicitly deferred §12.3 line 93/99 to the uncovered-region pass. The comment "Same, different internal routing" for P_LOGIC_B_FB is imprecise (it is logic-level B input with feedback output, not merely 'different 
