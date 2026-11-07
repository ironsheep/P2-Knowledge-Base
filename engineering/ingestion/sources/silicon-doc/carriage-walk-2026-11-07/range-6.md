# Silicon Doc walk, range 6: SD:3702-4253

Smart pins overview, pin configuration modes, smart pin modes %00000 to %10111 (the range ends inside the %10101-%10111 section).
YAML read: `architecture/smart_pins.yaml` (whole), `architecture/smart-pins/smart-pin-00000` to `-10111` (all 24 pages in full), `architecture/smart_pin_patterns.yaml:160-190`, `architecture/pin-drive-configuration.yaml:1-130`, `language/pasm2/{wrpin,rdpin,rqpin,akpin,wxpin,wypin}.yaml` (whole), `language/pasm2/concepts/basic-io.yaml:280-300,380-395`, `language/pasm2/concepts/multi_cog_synchronization.yaml:262-290`, `language/pasm2/concepts/streamer_smartpin_control.yaml:280-295`, `language/spin2/methods/{wypin.yaml:80-100, wxpin.yaml:140-160, pinstart.yaml:120-135}`.

## Sections

| SD line | Heading | Disposition |
|---|---|---|
| 3702 | SMART PINS | Mostly carried well in `smart_pins.yaml`. Gaps: write-only/read-only register rule, the Z-MSB fallback for C, and the multi-cog bus-timing rule lives only on `basic-io.yaml`. The `%TT` constants block has context-free descriptions that are wrong for `P_BITDAC`'s own context. |
| 3865 | PIN CONFIGURATION MODES | 13-bit M field carried (`pin-drive-configuration.yaml`). Odd/even adjacent-pin wiring of the pin circuit is only partly carried. |
| 3873 | Equivalent Schematics for Each Unique I/O Pin Configuration | Images only, no text in the extract. Not compared (mechanism). |
| 3904 | SMART PIN MODES (%00000 to %10111) | Mode semantics match on every page. Defects are in the worked examples (repository written with WYPIN on 3 pages, PINSTART into repository, pulse "N pulses" with continuous-high X, %01111 AKPIN "clear counter", %10101 unrouted second pin) and in two unsourced generalisations (NCO-duty phase during reset, P_FILT1 "2-clock"). |

## Ledger

| SD lines | Fact (one line) | Contract/Mechanism | YAML home (file:line) or NOT-CARRIED | Disposition | Note (quotes, searches) |
|---|---|---|---|---|---|
| 3704 | Each pin has an autonomous smart-pin circuit | Mechanism | smart_pins.yaml:33-35 | MATCH | "64 identical smart I/O pins, each with autonomous processing" |
| 3706 | In smart modes DIR is an active-low reset; output enable comes from a config bit; OUT ignored when the smart pin drives; IN is a handshake flag | Contract | smart_pins.yaml:37-40, :249-258, :412 | MATCH | "x0=disabled regardless of DIR, x1=enabled regardless of DIR"; IN "a HANDSHAKE, not the pin's logic level" |
| 3708-3713 | mode, X, Y are write-only; Z is read-only | Contract | NOT-CARRIED (smart_pins.yaml:437-458 lists X/Y/Z with widths and usage only) | NOT-CARRIED | Searched "write-only", "write only", "read-only", "cannot be read back" over smart_pins.yaml, smart-pins/, w?pin/r?pin pages: no hit. Most likely page: smart_pins.yaml `x_y_z_registers` |
| 3715-3722 | WRPIN/WXPIN/WYPIN/RDPIN/RQPIN/AKPIN are 2-clock; S selects pin 0..63; RDPIN acks, RQPIN does not | Contract | wrpin.yaml:8-10; rdpin.yaml:153-166; rqpin.yaml:192-212; akpin.yaml:217-229 | MATCH | rdpin "acknowledge smart pin"; rqpin oneliner "without acknowledge"; all `cycles: 2` |
| 3725 | Cogs' 34-bit buses to a pin are OR'd; cogs doing WRPIN/WXPIN/WYPIN/RDPIN/AKPIN on one pin must do so at different times; any number may RQPIN at once | Contract | language/pasm2/concepts/basic-io.yaml:392 (and spin2 twin :383); smart_pins.yaml:259-261, :474-475 | PARTIAL | basic-io: "Smart-pin write buses (WRPIN/WXPIN/WYPIN/RDPIN/AKPIN) are OR'd the same way; use RQPIN ...". The rule "must do so at different times" and the 34-bit bus are not on smart_pins.yaml, wrpin, wxpin, wypin or rdpin, the pages a code-writer reads. Searched "34-bit", "clobber", "different times", "same smart pin" |
| 3727 | Pin's outgoing 33-bit bus carries Z and a flag; C gets a mode flag **or the MSB of Z** | Contract | smart_pin_patterns.yaml:181 (33-bit bus); rdpin.yaml:165,168 "C = modal result" | NOT-CARRIED (MSB half) | No page says C = Z[31] in modes without a special flag. Searched "MSB of Z", "MSB of the Z", "mode-related flag", "Z\[31\].*C". Most likely pages: rdpin.yaml/rqpin.yaml `flags_affected.C` |
| 3729-3755 | WRPIN D = %AAAA_BBBB_FFF_M13_TT_SSSSS_0; A/B selector table | Contract | smart_pins.yaml:297, :323-342; wrpin.yaml:32, :45-60 | MATCH | Rows identical, including "x100 = this pin's OUT bit from cogs" |
| 3757-3767 | %FFF logic/filter table; resultant A drives IN in non-smart modes | Contract | smart_pins.yaml:203-214, :343-356 | MATCH | Rows identical |
| 3769-3770 | %M..M low-level pin control | Contract | pin-drive-configuration.yaml:61, :83-88 | MATCH | "Thirteen bits of the WRPIN D operand -- %M..M, D[20:8]" |
| 3776-3778 | OTHER: odd pin = even pin's NOT output; even pin = unique PRN bit; SMART overrides OUT/OTHER | Contract | smart_pins.yaml:374-377 | MATCH | |
| 3779-3780 | DAC_MODE when M[12:10]=%101; BIT_DAC = {2{M[7:4]}} / {2{M[3:0]}} | Contract | smart_pins.yaml:364-365 | MATCH | |
| 3782-3793 | %TT with smart pin off (non-DAC and DAC_MODE rows) | Contract | smart_pins.yaml:398-409 | MATCH | %00 row adds "DIR enables the DAC output", sourced to the datasheet and EF-055 |
| 3795-3797 | All smart modes: TT x0 = output disabled, x1 = enabled, regardless of DIR | Contract | smart_pins.yaml:412, :417 | MATCH | |
| 3799-3801 | DAC smart modes: 0x OUT / 1x OTHER enables ADC, M[7:0] overridden | Contract | smart_pins.yaml:418-422 | MATCH | Plus erratum E6 (EF-071): OUT needs TT bit 0 |
| 3803-3805 | Non-DAC smart modes: 0x SMART/OUT, 1x SMART/OTHER, or BIT_DAC in DAC_MODE | Contract | smart_pins.yaml:413-414 | MATCH | |
| 3782-3805 | Per-constant TT meanings | Contract | smart_pins.yaml:379-396 | MISMATCH | `P_TT_10` (alias `P_BITDAC`): "Output disabled, OTHER source selected". SD:3792 (smart off, DAC_MODE, the alias's own context): "10 = OUT drives BIT_DAC". `P_TT_00`: "output controlled by DIR/OUT", but SD:3796 says in smart modes x0 = "output disabled, regardless of DIR". The block states one context per constant with no context named; the table at :397-418 below it is right |
| 3807-3841 | %SSSSS mode list | Contract | smart_pins.yaml:55-100 | MATCH | All 32 rows |
| 3843 | `*` modes override OUT (%00100-%01010, %11011, %11100, %11110) | Contract | `out_signal`/`out_override` in smart-pin-00100..01010, 11011:81, 11100, 11110 | MATCH | No page in the starred set lacks it, and no unstarred page claims it |
| 3845 | Event raises IN; WRPIN/WXPIN/WYPIN/RDPIN/AKPIN ack and lower IN; RQPIN does not | Contract | smart_pins.yaml:249-261, :466-478 | MATCH | Quoted verbatim |
| 3847-3851 | IN takes 2 clocks to drop after an ack; NOP then TESTP | Contract | wrpin.yaml:12-18; rdpin.yaml:156-164; smart_pins.yaml:262-264 | MATCH | |
| 3854 | Configure with DIR low, then raise DIR; then feed WXPIN/WYPIN or read RDPIN/RQPIN | Contract | smart_pins.yaml:103-140, :575-581 | MATCH | |
| 3856 | DIR low resets but keeps WRPIN config; 126 state bits are muxed by %SSSSS; WRPIN with DIR high is unpredictable | Contract | smart_pins.yaml:141-165 | MATCH | |
| 3858 | While configured, %TT governs output enable regardless of DIR | Contract | smart_pins.yaml:412 | MATCH | |
| 3860 | Reset without reconfiguring: clear then set DIR | Contract | smart_pins.yaml:154-165 | MATCH | |
| 3862 | `WRPIN #0,pin` returns a pin to normal mode | Contract | wrpin.yaml:24, :63, :79; smart_pins.yaml:39-40, :110; basic-io.yaml:289 | PARTIAL | YAML: "Exception: WRPIN #0 resets a running smart pin without a DIR cycle". SD says only "return a pin to normal mode". The "exception to configure-while-DIR-low" framing is an inference, cited to "SMART PINS", which does not say it. Not contradicted |
| 3867 | 13 config bits M[12:0] = D[20:8]; some smart modes partly overwrite them (e.g. DAC values) | Contract | pin-drive-configuration.yaml:61, :85; smart-pin-00011:216 ("overrides M[7:0]") | MATCH | |
| 3869 | Pin circuit is powered from its local 3.3 V pin and connects to its odd/even partner (P0<->P1, P2<->P3) | Contract (minor) | smart_pins.yaml:375 (OTHER only); smart-pin-11011:14 (USB pair only) | PARTIAL | The general rule, that the low-level circuit sees its partner pin, is not on pin-drive-configuration.yaml. Searched "P0 and P1", "odd/even adjacent", "pin pair", "local 3.3V" |
| 3873-3902 | Equivalent schematics | Mechanism | n/a | not compared | Image-only in the text extract |
| 3906 | %SSSSS sits in D[5:1] | Contract | smart_pins.yaml:431-435 | MATCH | |
| 3908-3910 | %00000 normal mode, no smart function | Contract | smart-pin-00000:15-24 | MATCH | |
| 3912-3914 | %00001-%00011 without DAC_MODE: long repository, **WXPIN** writes the long, RDPIN/RQPIN read it | Contract | smart-pin-00001:170-174; smart_pin_patterns.yaml:182 | MATCH | "x_register: 32-bit value to store (written by WXPIN)" |
| 3914 | (same fact, other pages) | Contract | multi_cog_synchronization.yaml:276; streamer_smartpin_control.yaml:291; language/spin2/methods/wypin.yaml:93 | MISMATCH | All three write the repository with WYPIN: `wypin data_value, #REPO_PIN`; `wypin data_value, repo_pin`; `P_REPOSITORY: "32-bit value to store"` under `mode_specific_y_values`. SD: "WXPIN writes the long" |
| 3916 | Active (DIR=1): WXPIN updates the long and raises IN | Contract | smart-pin-00001:174 | MATCH | "Raised when WXPIN writes the long (DIR=1)" |
| 3918 | Reset (DIR=0): WXPIN ignored, IN low | Contract | not on smart-pin-00001 | IN-PLAN §7 | §7's reset_preload table spans SD:3918 |
| 3918 | (same fact, worked example) | Contract | smart-pin-00001:202; pinstart.yaml:132 | MISMATCH | Example `PINSTART(REPO_PIN, mode, $12345678, 0)  ' Store value in X`. PINSTART writes X before DIR rises (pinstart.yaml:124-129), and SD:3918 says that write is ignored. pinstart.yaml:132 calls PINSTART "Complete initialization for value modes" with no repository exception |
| 3845 | RDPIN acks (lowers IN) | Contract | smart-pin-00001:219 | MISMATCH | `value := RDPIN(REPO_PIN)        ' Read without clearing IN`. RDPIN clears IN (SD:3845); RQPIN is the call that does not |
| 3921-3929 | DAC noise: overrides M[7:0]; needs M[12:10]=%101; pattern unique per pin; X[15:0] period (0 = 65,536); RDPIN = 16-bit ADC accumulation; reset IN low | Contract | smart-pin-00001:176-182 | PARTIAL | All carried except "Each pin in this mode receives a unique data pattern" (searched "unique data", "unique pattern"). Reset half is IN-PLAN §7 |
| 3932-3946 | PRNG dither: X period; Y[15:0] captured each period, IN raised; X=1 for immediate effect (IN stays high); OUT high enables ADC; reset IN low, Y captured | Contract | smart-pin-00010:33-57 | MATCH | "Sample period (1 = immediate updates, IN stays high)"; "IN=0, Y[15:0] captured during reset" |
| 3949-3963 | PWM dither: X multiple of 256; Y captured; Fclock/256 at -48 dB; reset IN low, Y captured | Contract | smart-pin-00011:214-254 | PARTIAL | Content matches. The quoted reason differs: YAML :220, :380 "a maximum of only two transitions occur for every 256 clocks"; SD:3959 "a maximum of only two adjacent 8-bit DAC levels are set". YAML quotes the PDF edition (part4-smart-pins.txt:301; also HW manual :1094); the DOCX text is the walked source. Same wording in p2an003:118 |
| 3966-3984 | Pulse/cycle: counter X[15:0] down to 1; high while counter > X[31:16] and Y>0; Y decrements per pulse; IN at Y=0; reset IN low, output low, Y=0 | Contract | smart-pin-00100:15-46 | MATCH | |
| 3978 | X[31:16]=0 gives output high for the whole duration of Y>0 | Contract | smart-pin-00100:55, :60-67, :102-110 | MISMATCH | `single_pulse(1000, 16)  ' 1000-clock pulse, 16 times` with `WXPIN(PULSE_PIN, width_clocks) ' X[31:16]=0`, and PASM `gen_pulses` "Generate N pulses of specified width" with "X[31:16] = 0 (continuous high)". By SD:3978 (and the page's own :156) this gives one continuous 16,000-clock high, not 16 pulses |
| 3987-3997 | Transition: base-period counter free-runs from leaving reset; all transitions are synchronised to it; toggle Y times starting at the next base period; IN when done, pin holds state; reset IN low, output low, Y=0 | Contract | smart-pin-00101:24-46 | PARTIAL | The free-running, synchronised base period is not stated, so the time to the first edge after WYPIN (anywhere up to one base period) is not documented. Searched "free-running", "synchroniz" on the page: only a y_zero/NCO mention |
| 4000-4014 | NCO freq: WXPIN writes X[31:16] to Z[31:16] even during reset; Y added each base period; output = Z[31]; IN on overflow | Contract | smart-pin-00110:15-43; spin2/methods/wxpin.yaml:151 | MATCH | Reset values (Z[15:0]=0) IN-PLAN §7 |
| 4017-4031 | NCO duty: WXPIN writes X[31:16] to Z[31:16] (no "even during reset"); output = overflow; reset sets **all** of Z to 0 | Contract | smart-pin-00111:213-243 (operation MATCH); spin2/methods/wxpin.yaml:151 | MISMATCH | wxpin.yaml:151: "In the NCO modes, WXPIN writes X[31:16] into Z[31:16] (the phase), even during reset". SD gives "even during reset" for %00110 only (SD:4006), and for %00111 says "During reset ... Z is set to zero" (SD:4031). So a phase written during reset is not documented to survive in duty mode. This is an inferred contradiction, not measured |
| 4034-4050 | PWM triangle: X base/frame; Y captured at frame start; counts down then up; update time = 2 frames; high when value >= counter | Contract | smart-pin-01000:9-32 | MATCH | "Output high when counter ≤ duty value"; "PWM period = 2 × frame period" |
| 4053-4067 | PWM sawtooth: counts 1 up to frame; same compare | Contract | smart-pin-01001:95-120 | MATCH | |
| 4053-4067 | (sawtooth page prose) | Mechanism | smart-pin-01001:105, :173; smart-pin-01000:86 | PARTIAL | "Fast rise, slow fall characteristic creates sawtooth pattern" and "Symmetrical rise/fall times due to triangle counting" have no source and describe a digital output's edges wrongly. Not contract |
| 4070-4091 | SMPS: A sampled each base period until low, then Y captured, IN raised; B high forces low for the rest of the cycle | Contract | smart-pin-01010:182-208 | MATCH | |
| 4093-4105 | Quadrature: X=0 continuous / X>0 periodic; residual 0/1/-1 carried; IN per period; zeroed by pulsing DIR low | Contract | smart-pin-01011:9-30, :93-98 | PARTIAL | Semantics match. "Counts all four transitions per encoder detent" and "4 counts per encoder detent" (:11, :27, :94) are unsourced and depend on the encoder. Reset Z IN-PLAN §7 |
| 3763 (filt1) | P_FILT1_AB uses global filt1 | Contract (minor) | smart-pin-01011:91 | MISMATCH | "P_FILT1_AB - Add 2-clock filtering". The KB's own filt1 default is "length 1 (3 flipflops), tap 5 (32:1), 600ns" (smart_pins.yaml:227) |
| 4108-4116 | %01100: count A rises while B high; periodic/continuous | Contract | smart-pin-01100:106-129 | MATCH | |
| 4119-4127 | %01101: A rises, B=1 inc / B=0 dec | Contract | smart-pin-01101:199-222 | MATCH | |
| 4130-4139 | %01110: Y[0]=0 count A rises; Y[0]=1 inc on A rise, dec on B rise | Contract | smart-pin-01110:13-45 | MATCH | |
| 4142-4151 | %01111: Y[0]=0 count A highs; Y[0]=1 inc A-high, dec B-high | Contract | smart-pin-01111:132-156 | MATCH | |
| 3706, 3845 | IN is a handshake in smart modes; AKPIN only lowers IN | Contract | smart-pin-01111:180-197 | MISMATCH | PASM "pulse width measurement" uses `testp #signal_pin wz ' Wait for low/high` on the pin running the smart mode (reads the handshake, not the level; smart_pins.yaml:249-251) and `akpin #signal_pin ' Clear counter`. AKPIN does not clear Z (SD:3845, akpin.yaml:217) |
| 4154-4162 | %10000: on each change, prior state to C, its duration to Z, IN raised; Z capped at $80000000; reset Z=1 | Contract | smart-pin-10000:9-33 | MATCH | "C flag indicates previous state (1=was high, 0=was low)" |
| 4160 | Overrun loses measurements; workaround is two pins timing highs, one with A inverted | Contract | smart-pin-10000:103-104 | PARTIAL | "Use two pins with inverted inputs to capture all transitions". SD's workaround is time-highs mode on both pins, with one inverted, and the sum of durations is still bounded by the cog's read rate |
| 4165-4171 | %10001: on high-to-low, high duration to Z, IN; cap; reset Z=1 | Contract | smart-pin-10001:113-137 | MATCH | |
| 4174-4188 | %10010, Y[2]=0: time until X highs/rises/edges (Y[1:0]); cap; reset Z=1 | Contract | smart-pin-10010:215-240 | MATCH | |
| 4191-4205 | %10010, Y[2]=1: timeout after X clocks without event; IN raised, new window; Z running count; event reloads Z=1 | Contract | smart-pin-10010:217-237 | PARTIAL | Matches. `acknowledge_restarts` (:241), "next measurement starts automatically ... back to back", has no source; SD says nothing about restart for the Y[2]=0 branch |
| 4208-4226 | %10011/%10100: X periods, Y[1:0] A/B rise/edge; coincident edge starts next period; result to Z, IN, new measurement; cap; reset Z=0 | Contract | smart-pin-10011:9-33; smart-pin-10100:106-135, :224 | MATCH | 10011:30 "$00000000 during reset". %10100 "states" read as clocks A is high, which fits SD's "complementary duty measurement". %10100 reset value IN-PLAN §7 |
| 4229-4250 | %10101/%10110/%10111: periods until X clocks elapse and the period in progress completes; time / A-states / period count | Contract | smart-pin-10101:9-25; smart-pin-10110:133-148; smart-pin-10111:258-271 | MATCH | |
| 4252 | At least two of these measurements must run concurrently | Contract | smart-pin-10111:403; 10101:15-19 | MATCH | |
| 4252 | (concurrent pairing, worked example) | Contract | smart-pin-10101:52-66 | MISMATCH | Comment "Both pins observe the same signal", but `pinstart(base_pin+1, P_COUNTER_HIGHS, window_clks, %00)` has no A/B routing, so pin 21 measures itself. The sibling page says of exactly this: "routing A alone leaves B on the cell's idle own-pin and IN never rises" (10110:181-183, 10111:345-348). The 10101 example hangs or returns another pin's data |
| 3918-4226 | Reset values (IN, output, Y, Z) for %00110, %00111, %01000-%01111, %10100 not on their pages | Contract | per-mode pages | IN-PLAN §7 | `z_register.reset_preload` table |

Totals: MATCH 40 · PARTIAL 10 · MISMATCH 9 · NOT-CARRIED 2 · IN-PLAN 2 · not compared 1.

## Findings

MISMATCH and NOT-CARRIED contract rows, most consequential first.

1. **Long repository written with WYPIN (3 pages). MISMATCH.**
   SD:3914: "This mode turns the smart pin into a long repository, where WXPIN writes the long and RDPIN/RQPIN can read the long."
   KB: `language/pasm2/concepts/multi_cog_synchronization.yaml:276` `wypin   data_value, #REPO_PIN`; `language/pasm2/concepts/streamer_smartpin_control.yaml:291` `wypin   data_value, repo_pin`; `language/spin2/methods/wypin.yaml:93` `P_REPOSITORY: "32-bit value to store"` under `mode_specific_y_values`. The mode page itself is right (`smart-pin-00001:171`). Code copied from the three pattern pages stores nothing. Search: `grep -rn -i repositor`.

2. **Repository loaded by PINSTART during reset. MISMATCH.**
   SD:3918: "During reset (DIR=0), WXPIN instructions are ignored and IN is low."
   KB: `smart-pin-00001:202` `PINSTART(REPO_PIN, mode, $12345678, 0)  ' Store value in X (xval)`. PINSTART writes X before raising DIR (`pinstart.yaml:124-129`), so the value is dropped. `pinstart.yaml:132` "Complete initialization for value modes" gives no repository exception. The same page's `:219` `RDPIN(REPO_PIN) ' Read without clearing IN` is also wrong: SD:3845 lists RDPIN among the acknowledging instructions.

3. **%10101 concurrent-measurement example watches the wrong pin. MISMATCH.**
   SD:4252: "At least two of these measurements must be made concurrently to get useful results."
   KB: `smart-pin-10101:52,59-60` "Both pins observe the same signal", then `pinstart(base_pin+1, P_COUNTER_HIGHS, window_clks, %00)` with no `P_MINUS1_A | P_MINUS1_B`. The KB's own sibling pages (`smart-pin-10110:181-183`, `smart-pin-10111:345-348`) say that without routing "IN never rises and the REPEAT UNTIL below hangs".

4. **%01111 PASM example: TESTP read as level, AKPIN as "clear counter". MISMATCH.**
   SD:3706: "The IN bit serves as a flag ..."; SD:3845: "A cog acknowledges a smart pin whenever it does a WRPIN, WXPIN, WYPIN, RDPIN or AKPIN on it. This causes the smart pin to lower its IN signal".
   KB: `smart-pin-01111:187-197` `testp #signal_pin wz ' Wait for low` / `' Wait for high` on the pin running `P_COUNT_HIGHS`, then `akpin #signal_pin ' Clear counter`. TESTP returns the handshake (`smart_pins.yaml:249-251`), and AKPIN leaves Z alone (`akpin.yaml:217`).

5. **Pulse mode "N pulses" examples produce one long high. MISMATCH.**
   SD:3978: "If X.[31..16] is set to 0, the output will be high for the duration of Y > 0."
   KB: `smart-pin-00100:55` `single_pulse(1000, 16)  ' 1000-clock pulse, 16 times` with `:65` `X[31:16]=0 for continuous high`; `:102-107` "Generate N pulses of specified width" with "X[31:16] = 0 (continuous high)". The page's own `:156` states the continuous-high rule the examples break.

6. **C on RDPIN/RQPIN: the Z-MSB case is missing. NOT-CARRIED.**
   SD:3727: "C will be either a mode-related flag or the MSB of the Z result."
   KB: `rdpin.yaml:165,168` and `rqpin.yaml:195,197` say only "C = modal result"; `smart_pin_patterns.yaml:181` quotes the 33-bit bus sentence and stops before it. Searched "MSB of Z", "MSB of the Z", "mode-related flag", "Z\[31\]". Home: `rdpin.yaml`/`rqpin.yaml` `flags_affected.C`.

7. **TT constant descriptions wrong in their alias's own context. MISMATCH.**
   SD:3792 (smart off, DAC_MODE): "10 = OUT drives BIT_DAC"; SD:3796 (smart modes): "x0 = output disabled, regardless of DIR".
   KB: `smart_pins.yaml:388-392` `P_TT_10 ... aliases: ["P_BITDAC"] ... "Output disabled, OTHER source selected"`. `P_BITDAC` is used in the smart-off DAC context, where %10 means OUT drives BIT_DAC with DIR enabling. `:379-382` `P_TT_00 "Default - output controlled by DIR/OUT"` is wrong in every smart mode. The context table at `:397-418` is correct; the constants block names no context.

8. **NCO duty phase "even during reset". MISMATCH (inferred).**
   SD:4006 (%00110 only): "X.[31..16] is written to Z.[31..16] to allow phase setting, even during reset". SD:4023 (%00111) leaves out "even during reset", and SD:4031 says "During reset (DIR=0) ... Z is set to zero".
   KB: `language/spin2/methods/wxpin.yaml:151` "In the NCO modes, WXPIN writes X[31:16] into Z[31:16] (the phase), even during reset". Writing a phase before DIRH in duty mode is not documented to survive. Either restrict the line to %00110 or measure it.

9. **Smart-pin registers are write-only (mode, X, Y) and read-only (Z). NOT-CARRIED.**
   SD:3710-3713: "mode ... (write-only) / X ... (write-only) / Y ... (write-only) / Z ... (read-only)".
   KB: `smart_pins.yaml:437-458` gives widths and usage only. Searched "write-only", "write only", "read-only", "cannot be read back" across the smart-pin and pin-instruction pages. Home: `smart_pins.yaml x_y_z_registers`.

10. **P_FILT1_AB called "2-clock filtering". MISMATCH (minor).**
    The KB's filt1 default is "length 1 (3 flipflops), tap 5 (32:1), 600ns" (`smart_pins.yaml:227`, which cites the Silicon Doc filter section); EF-095 gives 4 clocks of delay even at tap 0.
    KB: `smart-pin-01011:91` "P_FILT1_AB - Add 2-clock filtering to reduce noise".

Also worth fixing in the same pass (PARTIAL, contract):
- The multi-cog "at different times" bus rule (SD:3725) is only on `basic-io.yaml:392`, not on `smart_pins.yaml` or the W*PIN/RDPIN pages.
- Transition mode's free-running, synchronised base period (SD:3991) is not on `smart-pin-00101`.
- `smart-pin-10010:241 acknowledge_restarts` has no source.
- `smart-pin-01011` "4 counts per detent" has no source.
- `smart-pin-00011:220` quotes the PDF-edition wording rather than the DOCX ("two adjacent 8-bit DAC levels are set").
