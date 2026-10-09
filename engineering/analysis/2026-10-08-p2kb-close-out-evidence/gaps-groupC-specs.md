# Close-out study, group C: knowledge gaps G-002 … G-029 (16 gaps)

Task «#407», group C. Study freeze: nothing in the KB, the ingestion tree or the register was edited.
Written 2026-10-09. Source paths below are relative to `engineering/ingestion/` unless they start with
`deliverables/` or `engineering/`.

Abbreviations: **SD** `sources/silicon-doc/silicon-doc-text.txt` · **HW** `sources/p2-hardware-manual/p2-hardware-manual-text.txt` ·
**DS** `sources/p2-datasheet/p2-datasheet-text.txt` · **PM** `sources/pasm2-manual/pasm2-manual-text.txt` ·
**TI** `sources/smart-pins-titus/smart-pins-titus-text.txt` · **CSV** `sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv` ·
**EF** `external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` · **VO** `…/VERIFICATION-OPPORTUNITIES.md` ·
**HDL** `external-inputs/p2-hdl-study/` (Rev C hardware-description study: **indicator only, never a citation**).

States: ANSWERED · BENCH QUESTION · OUT OF REACH · ALREADY CLOSED.

New sources searched that did not exist when most gaps were filed: the v55 interpreter
(`external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2`), the v51 debugger
(`external-inputs/source-code/spin-debugger/v51/Spin2_debugger.spin2`), `spin2-v55-operator-reference.md`, EF-001..EF-0xx,
the HDL study. None of the three code/operator sources bears on any of the 16 gaps (searched: stack/stk, usb, smps, nco,
dither, lut+pin; the only hits are the debugger's 8 POP / 8 PUSH save/restore of the hardware stack, `Spin2_debugger.spin2:315-322`,
`:400-407`, which is data movement and says nothing about a 9th push).

---

## Summary table

| Gap | Subject | State | Row / bench id |
|---|---|---|---|
| G-002 | DAC dither cadence / ENOB | cadence ANSWERED (already carried); ENOB OUT OF REACH | Q-008 (exists) |
| G-004 | %01010 SMPS Y timing / code example | Y-timing ANSWERED (carried); example: none exists to ingest; KB's own example is unsourced and wrong | S-003, S-230, S-300, S-304 (+ 1 new defect, see G-004) |
| G-005 | USB scope / sysclk floor | scope ANSWERED; FS>80 MHz claim OUT OF REACH | Q-003 (exists) |
| G-006 | NCO Y=0 / jitter | Y=0 on %00110 ALREADY CLOSED (EF-013); %00111 Y=0 and jitter: two small BENCH questions | VO-G006a, VO-G006b (new) |
| G-009 | HyperRAM/Flash part numbers | ANSWERED (read from the rendered page; one string is wrong in the KB) | new row (see G-009) |
| G-012 | add-on `+N` offsets | ANSWERED (convention read from figures) | — |
| G-015 | add-on example code | OUT OF REACH (archives not held) | ingestion-head backlog |
| G-019 | I/O AC timing | OUT OF REACH | Q-007 (exists) |
| G-020 | thermal / layout | PARTLY ANSWERED (layout half exists, gap row is wrong); thermal figures OUT OF REACH | new row (see G-020) |
| G-022 | mikroBUS TX/RX, rails | OUT OF REACH (document not held: mikroBUS spec) | new Q-010 proposed |
| G-023 | SMPS 'A' polarity | ANSWERED (low); row mislabels the mode | — |
| G-024 | SETS/SETD/SETR hazard | ALREADY CLOSED (rule sourced and carried); hazard mechanism OUT OF REACH; optional bench | VO-G024 (optional) |
| G-025 | BITC with index > 31 | ANSWERED; KB gap in 6 pasm2 pages | new row (see G-025) |
| G-027 | USB WRPIN without reset | BENCH QUESTION (sources disagree by edition) | VO-F372 (S-324), wording to correct |
| G-028 | 9th hardware-stack push | BENCH QUESTION (sources silent, pure silicon) | VO-G028 (new) |
| G-029 | LUT "data source for smart pins" | OUT OF REACH (designer) | new Q-011 proposed |

Bench questions in this file: VO-G006a, VO-G006b, VO-G028 are new; VO-G024 is optional; VO-F372 is existing.
None of the existing bench ids VO-S304, VO-J-028, VO-F337, VO-S037, VO-S059, VO-S337, VO-S157, VO-S367 duplicates a group-C gap
(VO-S304 touches %01010's register range, not G-004's question; VO-J-028 is Y-before-DIRH in counter modes, not G-006).

---

## G-002 — Smart Pins / DAC dither

**Unknown:** dithered-DAC update cadence (sysclk or sysclk/256) and the real effective resolution behind "16-bit".

**State: cadence ANSWERED (and already carried); ENOB OUT OF REACH.**

Evidence (read at the line):
- SD:3934 "feed the pin's 8-bit DAC with pseudo-randomly-dithered data on every clock"; SD:3936 "X.[15..0] establishes the sample period in clock cycles";
  SD:3938 "Y.[15..0] … captured at each sample period"; SD:3942 "set X.[15..0] to one (IN will stay high)" for immediate updates.
- SD:3951 PWM mode "PWM-dithered data on every clock"; SD:3953 "The sample period must be a multiple of 256 (X.[7..0]=0)"; SD:3959 "a frequency of Fclock/256 will be present in the output at -48dB".
- Same text at HW:1080, :1084, :1090-1094.
- So the dither itself runs every clock in both modes; X is only the Y-capture period; the multiple-of-256 rule belongs to PWM dither only.
- ENOB: searched `ENOB`, `effective resolution`, `effective number`, `dither` in SD, HW, DS, TI, PM, EF, VO. Every ENOB hit is the ADC/SINC tables
  (SD:4286, :4385, HW:1278, :1297 …), none is DAC dither; control hit proving the term works: SD:4385. No ENOB figure, no dither formula, no EF entry
  (EF-071 is the `TT`/ADC-enable finding, not resolution). A measurement would need an external instrument (catalogued, not run); the P2's own ADC cannot
  separate its noise from the DAC's.

KB impact: none needed for the cadence.
`smart-pin-00010-dac-16bit-pseudo-random-dither.yaml:187-189` ("Dithering occurs every clock cycle / No fixed period required / Sample period only affects Y capture timing") and
`smart-pin-00011-dac-16bit-pwm-dither.yaml:24,37-38` already state it. `p2an003-dac-analog-signal-generation.yaml:115` already says no ENOB is asserted.
Minor, optional: HW:1094 says "a maximum of only two transitions occur for every 256 clocks" while SD:3959 (newer edition) says "only two adjacent 8-bit DAC levels are set for every 256 clocks";
the KB (`smart-pin-00011…yaml:27,187`) uses the HW wording. Not contradictory; the SD wording is the later edition.

Cross-reference: Q-002 (design intent), Q-008 (ENOB). Not a study row.

---

## G-004 — Smart Pins / %01010 SMPS

**Unknown:** no code example anywhere; Y-register update timing unstated.

**State: Y-timing ANSWERED (already carried). Code example: nothing exists in any source to ingest (OUT OF REACH as an ingestion fact); the KB's own example is unsourced and defective.**

Evidence:
- SD:4078 "Y.[15..0] … captured at each frame start and used for its duration"; SD:4080 "the 'A' input is sampled at each base period until it reads low. After 'A' reads low, Y.[15..0] is captured, IN is raised";
  SD:4084 "it may be appropriate to just set Y.[15..0] once"; SD:4089 "WYPIN … internally captured at the start of every PWM frame".
  Same at HW:1156-1165 and TI (Jon Titus extract in `smart-pins-catalog/ingestionSources/mode-01010-pwm-smps/john-titus-extract.md:132`: "I DON'T KNOW ENOUGH ABOUT SMPSS … --JON").
- Example search: `P_PWM_SMPS` across all of `engineering/ingestion` (.spin2/.txt/.md). Hits are symbol tables only (`spin2-v55-text.txt:1540`, `spin2-v51-narrative.txt:5194`, PM:6468 …),
  plus one style sample `new-external-sources/Code Documentation Style/johnny-mac-documentation-style-complete.md:270` (`wrpin ##P_PWM_SMPS, alarm_pin ' set alarm pin to PWM` / `wxpin alarm_duty … 'set duty cycle`):
  a documentation-style illustration, not an SMPS design, and its X/Y use contradicts SD:4074-4078. Not a source. Control hit: the symbol-table hits prove the term finds the mode.
- HDL (indicator): `aspects/SMART-PIN-MODULATION-ENGINE.md:276-279` "A high A input at the top of the frame stalls both the step and the frame event, so the ramp parks at the top until A goes low".

KB impact, `deliverables/ai/P2/architecture/smart-pins/smart-pin-01010-pwm-smps.yaml`:
- `:37-73` the "Basic SMPS Controller Setup" block has no source. Defects already on the study: S-003 (`dirh()` is not Spin2, `:51`, `:56`), S-230 (A/B wired the wrong way round: `P_MINUS1_A` is pin 19 = `i_sense`, `P_PLUS1_B` is pin 21 = `v_sense`, `:44-45`, `:59`; SD:4090-4091 makes A the voltage detector and B the over-current detector), S-300 (`:39` "100kHz").
- NEW (not on the study): `:16` "Base period = System clock ÷ X[15:0] clock cycles" and `:23` "Base period divisor" are wrong; SD:4074 and HW:1152: "X.[15..0] establishes a base period in clock cycles". Correct: base period = X[15:0] sysclk cycles; frame = X[31:16] base periods.
- Recommendation: rebuild the example from SD:4070-4091 only if it is compiled and bench-verified (jumper, free pins; EF/XF), else delete it. No new bench question: this is authoring, not an unknown fact.
- S-304 (`:23-24` "1-65536") remains bench question VO-S304.

Cross-reference: S-003, S-230, S-300, S-304 (VO-S304).

---

## G-005 — Smart Pins / %11011 USB

**Unknown:** scope of smart-pin USB support; documented sysclk floor (FS-USB > 80 MHz).

**State: scope ANSWERED; the ">80 MHz floor" and "needs SW help" claims are OUT OF REACH (Q-003).**

Evidence:
- Scope: SD:4577-4593 (pair DM/DP, `%1_11011_0` / `%0_11011_0` sniffer, WXPIN D[15] host/device, D[14] full/low speed, D[13:0] baud, DP raises IN when the FIFO has room, start sequence); HW:1487-1489; DS:127; TI:1382-1384.
- sysclk dependency: SD:4587 "a 16-bit fraction of the system clock (ie (12_000_000 FRAC clkfreq) >> 16), whose two MSBs must be 0, necessitating that the baud rate be less than 1/4th of the system clock frequency" (same HW:1489).
- Floor: searched `80 ?MHz` in SD, HW, DS, TI, spin2-v55: the only hits are the worked example (SD:4587, HW:1489, TI:1384, a sysclk of 80 MHz chosen for the arithmetic) and unrelated lines (SD:1874, SD:4881 FPGA). Control hit: those example lines. No source states a floor or that implementation needs software help. HDL has no sniffer/floor text (searched `sniff`).

KB impact: none. `smart-pin-11011-usb-host-device.yaml:30-31,43-44` carry the < sysclk/4 rule and the 80 MHz example, labelled as an example; they assert no floor.
(Observation, not a defect: SD:4587 prints `WXPN ##$C000 | $2666,lowerpin`; the typo `WXPN` is in the ingested text and the KB correctly uses `$E666`.)

Cross-reference: Q-003 (exists). Not a study row.

---

## G-006 — Smart Pins / NCO

**Unknown:** is `Y=0` valid for NCO (%00110/%00111) (continuous output or none); NCO quantisation jitter.

**State: `Y=0` on %00110 ALREADY CLOSED by a bench result; `%00111` `Y=0` and the jitter half are two small BENCH QUESTIONS (pure silicon).**

Evidence:
- **EF-013** (`EF:257-260`): "NCO with Y=0 produces NO output (static) — CONFIRMED … `batch1` RA-12 — `Y=0 events=0`, control (Y>0) `events=200`." Rig `campaigns/2026-06-debug-windows-and-smart-pins/tests/smart-pins/iosp-titus-verification-batch1.spin2:89` uses `P_NCO_FREQ | P_OE` only. This closes the Titus reviewer #8 question for **%00110**; the gap row (last re-tested 2026-08-26) predates reading it.
- Sources are silent on both Y=0 (SD:4008, HW:1116-1131 state only "Y added into Z at each base period") and jitter: searched `jitter`, `quantiz` in SD, HW, DS, TI. Hits are PLL jitter (SD:54, :81, control) and HW:187 (unrelated). Reviewer #17's arithmetic is a lead (`smart-pins-titus/reviewer-comments-harvest.md:40`), not a source.
- KB: `smart-pin-00110-nco-frequency.yaml:32` already states "Y = 0 produces NO output". `smart-pin-00111-nco-duty.yaml` has no Y=0 statement (grep `Y *= *0|zero|jitter` returns nothing).

KB impact: none now. After VO-G006a, `smart-pin-00111-nco-duty.yaml` gains one line at its Y register block, cited to the new EF. Do not copy the %00110 result across by inference.

**VO-G006a (new, small).** Does `P_NCO_DUTY | P_OE` with `Y=0` raise IN or move the output? Extend the RA-12 rig with `P_NCO_DUTY`; arms Y=0 and Y>0 control; count IN events with `TESTP`. **Pure silicon, no pins** (IN is an internal flag). Search record above.

**VO-G006b (new, low priority; KB depends on nothing).** NCO interval jitter: with `P_NCO_FREQ`, `Y` not a divisor of 2^32, record the clock count between successive IN events (`GETCT` + `TESTP`) over a few thousand events; report the set of distinct intervals. **Pure silicon, no pins.** Recommendation: file only if Stephen wants jitter stated; the KB makes no jitter claim today.

---

## G-009 — Hardware / 64004-ES (OCR-transcribed part numbers)

**Unknown:** exact HyperRAM / HyperFlash part numbers and datasheet URLs (OCR risk).

**State: ANSWERED, by reading the rendered page (the corpus holds the PDF; the OCR text is the weak copy). One KB string is wrong.**

Evidence: `sources/hyperRam-n-hyperFlash/64004-ES P2-ES Eval HyperRAM_Flash Memory Board Product Guide.pdf`, **page 7 of 9 ("Resources and Downloads")**, rendered at 400 dpi and read:
- "Datasheet for HyperRAM (IS66WVH16M8BLL-100B1LI)" and `http://www.issi.com/WW/pdf/66-67WVH16M8ALL-BLL.pdf`
- "Datasheet for HyperFlash (IS26KL256S-DABLI00)" and `http://www.issi.com/WW/pdf/26KS-KL128S-256S-512S.pdf`
  The temperature-grade letter in the Flash string is a capital **I** followed by two zeros (`…-DABLI00`), the same `LI` letters as the RAM string's `…B1LI`; it is not the digit one.
- The OCR copy is wrong exactly where the gap feared: `sources/hyperRam-n-hyperFlash/hyperram-hyperflash-text.txt:153` reads `DABLl00` (lower-case L) and `:155` reads `issi.c0m` (zero). The ingested text stays as is (never edit ingested docs); this is a finding for the ingestion head.
- The 64004-ES Rev A schematic PDF (same folder) carries no part numbers (one page read: U100 "16MB HyperRAM", U101 "32MB HyperFLASH", BGA-24), so it is no second source.
- Not checked: the ISSI datasheets themselves (not held; we do not probe the vendor site from here). The strings are verified against the Parallax guide, which is the source the KB cites.

KB change, `deliverables/ai/P2/hardware/addon-hyperram-hyperflash.yaml`:
- `:153` `hyperflash: "ISSI IS26KL256S-DABL100 [VERIFY]"` → `"ISSI IS26KL256S-DABLI00"` (cite: 64004-ES Product Guide p.7).
- `:151`, `:152`, `:154` remove `[VERIFY]` (the strings match page 7 exactly); `:150` `verify_status` and `:170` "Datasheet part numbers/URLs are OCR-transcribed and unverified" → "read from the rendered page 7 of the Parallax product guide; not cross-checked against the ISSI datasheets".
- `:75` (the forced-OCR explanation) stays true as history.

---

## G-012 — Hardware / add-on `+N` offset

**Unknown:** what absolute P2 I/O each `+N` maps to.

**State: ANSWERED, with the rule read from figures (no text states it outright).**

Evidence chain:
- `sources/hyperRam-n-hyperFlash/64004-ES … Product Guide.pdf` p.8 pin table uses `IO+0 … IO+15` for the add-on, and p.3 prints the add-on's own headers as `7 6 / 5 4 / 3 2 / 1 0` (header 1A) and `15 14 / 13 12 / 11 10 / 9 8` (header 1B), `VIO3V3 5V` at the top and `GND GND` at the bottom. The add-on is stacked on two Eval headers (p.1 text, "stack on top of two P2-ES Eval Board I/O Pin Breakout Edge Headers"); step 3 "assert the RESET# signal High (IO+15)".
- The 64004-ES schematic (one page read) names the add-on sockets `J100` = `IO+0…IO+7`, `J101` = `IO+8…IO+15`.
- Eval Board guide, `sources/p2-eval-board/complete-p2-eval-board-reference.md:236-239`, from p.17: the P0–P7 header reads `GND/GND · P0/P1 · P2/P3 · P4/P5 · P6/P7 · 5V/V0007`. Rotated 180 degrees it reads `V0007 5V / P7 P6 / … / P1 P0 / GND GND`, which is the add-on's printed layout exactly: an add-on seated on the P0–P7 header puts `+0` over P0 and `+7` over P7. (I read the add-on side from the PDF page; I did not re-read Eval p.17.)
- `sources/p2-microSD-addon/complete-p2-microSD-addon-reference.md:60-64` states the convention the ingestion head derived: base pin = lowest I/O of the header the board sits in (P56 → 56–63).

Rule: **`+N` = the N-th I/O of the host header the add-on is seated on, counted from that header's lowest-numbered pin** (header P0–P7: +N = PN; P56–P63: +N = P(56+N); a two-header add-on spans a 16-pin pair, `+8…+15` on the upper header). The earlier "adverse evidence" (header orientation varies) does not break this: the add-on rotates with the header, which is why the positional mapping holds.

KB impact (optional, from the same rule): the add-on records' `+N` notes (e.g. `addon-microsd.yaml:36` "On the P2 programming header (base pin 56) …") may state the general rule once, in `hardware/hardware-compatibility-matrix.yaml`, citing the HyperRAM guide p.3/p.8 and Eval guide p.17. The per-add-on pin lists stay relative.
Caveat to carry: the rule is read from figures; it was verified for the HyperRAM add-on's layout only. Other add-ons carry their own `+N` silkscreen and are assumed to follow the Parallax convention; one Eval-board photo per add-on would confirm.

---

## G-015 — Hardware / add-on example code

**Unknown:** driver/init code for the add-ons is deferred to product-page downloads.

**State: OUT OF REACH.** It is an ingestion backlog item, not a KB fact.

Evidence: `sources/` holds the guides only. Example archives are staged and not committed for RTC #64013, HD-Audio #64014 and WX #32420 (`sources/P2-RTC-Add-on/NO-COMMIT`, `sources/P2-HD-Audio-Add-on/NO-COMMIT`, `sources/parallax-wx-wifi/NO-COMMIT`). The **#64009 microSD** and **#64010 Universal Motor Driver** example archives are not held at all (`find` of both source folders: guides, audits, assets only). The Eval, microSD and motor-driver guides carry no code.
What closes it: (1) the ingestion head runs a code-pass ingestion of the three staged archives; (2) someone supplies the microSD and motor-driver product-page archives. No YAML change is specified from this row.

---

## G-019 — Electrical / I/O AC timing

**Unknown:** I/O-pin propagation delay, rise/fall time, slew, per-drive-mode mA.

**State: OUT OF REACH** (needs Parallax-published numbers, or an external-instrument measurement: catalogued, not run).

Re-test against the sources now held: searched `propagation delay`, `rise time`, `fall time`, `slew rate` across `sources/` and `external-inputs/` (.md/.txt) and EF/VO. P2 pin hits: none. Hits are components (`p2-universal-motor-driver-text.txt:333-334` gate driver "~20ns propagation delay … 7.2ns rise, 5.5ns fall", control hit proving the terms find text) and two **derived notes that are not sources**:
`sources/p2-complete-signal-flow-matrix.md:155` "Rise Time: <2ns" and `sources/p2-addon-board-circuit-knowledge.md:395` (a 74HCT244). Neither may be cited as a P2 pin characteristic; the first is exactly the shape of the fabrication the row warns about. HDL is RTL and carries no analog timing.

KB impact: none; keep `architecture/io_pin_timing.yaml` free of ns/mA pin figures. Cross-reference: Q-007 (exists), F-327, F-329.

---

## G-020 — Design guidance / thermal + layout

**Unknown:** the datasheet raises thermal/power design and answers none of it.

**State: PARTLY ANSWERED (the row's "no layout/decoupling guidance" is wrong); thermal resistance, derating and EMC remain OUT OF REACH.**

Evidence the row missed (it searched `decoupl`, not `bypass`):
- DS:331 "All VDD and all Vxxyy pins must have closely-located bypass caps to GND (not shown)."
- DS:332-333 "The common GND (EP) pad under the chip is also used for thermal dissipation. It is recommended to connect the GND pad to a solid ground plane with multiple vias."
- DS:327-336 (whole Minimal Connections list: VDD one 1.8 V supply, Vxxyy 3.3 V, TEST to GND, RESN pull-up ~10 kΩ); DS:286-288 "Connect to ground plane for thermal dissipation"; DS:262-266 Parallax recommends the Edge module or Eval board "that includes all the recommended connections and layout design rules".
- Still absent: thermal resistance, derating curve, EMC. Searched `thermal resistance`, `junction-to`, `theta`, `derat`, `EMC` in SD, DS, HW. A derived note `sources/p2-board-power-analysis-matrix.md:143` "Thermal Resistance (θJA): 20°C/W" is **not a source** (analysis note; no provenance; the datasheet has no such figure). It must not reach the KB.

KB impact: `deliverables/ai/P2/` carries none of DS:327-336 (grep `bypass|Minimal Connections|exposed pad|ground plane` over `hardware/` and `architecture/` finds only `p2-package-mechanical.yaml:92`, the negative statement). Add a "minimal connections and layout" fact block to `hardware/p2-package-mechanical.yaml` (or a sibling), each line cited to DS:327-336. Keep `p2-package-mechanical.yaml:92` (no θJA).
Correct the gap row (see Proposed updates). Cross-reference: not a study row.

---

## G-022 — Hardware / mikroBUS Click #64008

**Unknown:** meaning of `TX`/`RX` on the Click socket; whether `5V_B`/`VIO_3V3_B` are commoned with the `_A` rails.

**State: OUT OF REACH.** Needs a document we do not hold: the MikroElektronika **mikroBUS standard specification** (socket signal naming and direction). The rail question is a netlist/continuity fact: the 64008 Rev A schematic does not draw it (`sources/p2-click-adapter/p2-click-adapter-netlist.md:82`, `:164`); only a continuity check on a board (external instrument, catalogued, not run) or Parallax closes it.

Search: `mikrobus` over `engineering/ingestion` (.md/.txt/.spin2/.pdf). Hits: the adapter's own docs, two Edge-board narratives ("Add Click / mikroBUS development"), a README and one OBEX driver header that merely links the adapter. No document states the standard's signal directions. Control hit: `netlist.md:113-114` (`RX | IO+3`, `TX | IO+2`). Peer evidence (the P2-Click-eInk driver; the Cricket ESP32 driver) is not an authority and its README says nothing on TX/RX.
Do not infer the convention from memory of the standard.

Proposed: new expert question **Q-010** (see Proposed updates). KB: `architecture/click_module_integration.yaml` keeps its crossover marked as peer-derived.

---

## G-023 — Smart Pins / counting mode 'A' polarity

**Unknown:** does IN rise when 'A' reads low or high. Note: the row's title says `%10xxx counting`; its quoted line (SD:4080) is the **%01010 SMPS** section.

**State: ANSWERED: low.**

Evidence (the row said no second source):
- SD:4080 "the 'A' input is sampled at each base period until it reads low. After 'A' reads low, Y.[15..0] is captured, IN is raised".
- SD:4090 (independent prose, same section): "When 'A' is low, a PWM cycle is performed because the final output voltage has sagged below the requirement and it's time to do another pulse." A high 'A' trigger would contradict this physical story.
- HW:1157 and TI (Titus extract line 149) repeat the polarity.
- HDL indicator: `aspects/SMART-PIN-MODULATION-ENGINE.md:362` "switch-mode supply | A | stalls the ramp and the frame event while high"; `:277-278` "the ramp parks at the top until A goes low".
- Reviewer [24] ("I think IN is raised when smartA is high") is one unnamed comment against three documents plus the stated mechanism; it is not a source. No bench is justified (the sources are not silent and do not disagree).

KB impact: none. `smart-pin-01010-pwm-smps.yaml:32,34,95` already say low.

---

## G-024 — PASM2 / SETS-SETD-SETR pipeline hazard

**Unknown:** may the "elapse two instructions" rule hide a one-NOP hazard (reviewer [12]).

**State: ALREADY CLOSED for the KB (the rule is sourced and carried). The reviewer's hazard mechanism is OUT OF REACH (a forum thread we do not fetch). An optional pure-silicon bench is described.**

Evidence:
- SD:669 "It is necessary to elapse two instructions before executing the modified register, due to pipelining"; SD:671-674 shows the two spacer `NOP`s.
- PM:3762, :3806, :3830 (SETD, SETR, SETS): "it is necessary to elapse **at least two** instructions before executing the modified register"; and the same family of rule for `DIRx` after DRVx, PM:2223 etc. ("not data-forwarded; the next pipelined instruction sees the old state").
- KB: `language/pasm2/sets.yaml:19-20`, `setr.yaml:14-16`, `setd.yaml:12-14` carry "at least two instructions".
- Searched `hazard`, `spacer`, `self-modif`, `dual-port` in SD, PM, HW, DS, spin2-v55, HDL (case-sensitive `SETS|SETD|SETR|ALTR`), EF and test sources. No source describes what a violated rule (one spacer) does. Control hit: SD:669.

Nothing in the KB needs to change. The hazard the reviewer mentions concerns doing less than the documented rule.
**Optional VO-G024 (pure silicon, no pins):** `SETR inst,op` followed by 0, 1 and 2 spacer `NOP`s then `inst`; record which instruction executed (old, new, or other). Value to the KB: low; recommend retiring unless Stephen wants the violated-rule behaviour stated.

---

## G-025 — PASM2 / BITC with bit index > 31

**Unknown:** is `BITC D,S` broken for a bit index above 31 since ADDPINS.

**State: ANSWERED from sources. It is not a break in BITC: it is the documented span field. The KB already carries the ALTB warning; six BITx pages omit the span rule.**

Evidence:
- CSV row 44: `BITC D,{#}S` = "Bits D[S[9:5]+S[4:0]:S[4:0]] = C. Other bits unaffected. Prior SETQ overrides S[9:5]." (`TESTB` rows 34-41 use `S[4:0]` only.)
- SD:60 "BITL/BITH/BITC/BITNC/BITZ/BITNZ/BITRND/BITNOT can now work on a span of bits (+S[9:5] bits). Prior SETQ overrides S[9:5]."
- PM:1501 "Src[4:0] indicates the bit number (0—31). For a range of bits … Src[9:5] indicates how many contiguous bits beyond the base should be affected (1–31)"; PM:1503 "When Src is a register, the register's value bits [9:0] are used as-is to form the 10-bit ID range, unless a SETQ … immediately precedes".
- The idiom in the reviewer's anchor, SD:556-557 `ALTB bitindex,#base` / `BITC 0,bitindex 'write C to bit[bitindex[4:0]]`, passes the same register as BITC's S. With `bitindex` > 31, bits [9:5] are non-zero, so BITC writes C to a **span** of bits instead of one. That is what ozpropdev saw; the commented `[4:0]` masks the base bit only. PM:1064 warns about exactly this: "BITxxx instructions … don't limit themselves to only reading Src[4:0] … the index value … will be misinterpreted as multiple bits to affect. One way to solve this is to use a SETQ #0 …".
- No compiler or bench probe is needed: the sources state it; a compiler cannot see silicon behaviour.

KB impact:
- `language/pasm2/altb.yaml:5` already carries the PM:1064 warning (ALREADY CLOSED on that page).
- Add the span rule (PM:1501-1504 text) to `bitc.yaml:12` and `bitnc.yaml`, and the matching entries `bith.yaml`, `bitl.yaml`, `bitz.yaml`, `bitnz.yaml` (their manual entries: PM:1521, :1539, :1557, :1577 repeat the same sentence). `bitnot.yaml:5` carries it; `bitrnd.yaml` carries it (grep `9:5|contiguous`: 4 and 1 hits; the other six: 0). Today `bitc.yaml:6-7,14-15` give `c`/`z` = "original D[S[4:0]]" with no span statement.
- Related, already on the study: S-202 (`register_indirection.yaml:75-81` misdescribes ALTB: PM:1052 says ALTB sets BITx's Dest to `(Src + Dest[13:5]) & $1FF`).

---

## G-027 — Smart Pins / USB WRPIN without reset

**Unknown:** can a new WRPIN reconfigure a running USB smart pin without resetting it.

**State: BENCH QUESTION (sources disagree by edition). The row's premise "no second source, same document" is wrong; the bench question on the study is worded for the wrong register.**

Evidence:
- The sentence "A new WRPIN can be done to effect such a change without resetting the smart pin" is in **three** ingested documents, not one: HW:1488 (P2 Hardware Manual @ 2022/11/01), TI:1382 (Smart Pins rev 5), and the older P2 Documentation (`sources/silicon-doc/p2-documentation.txt:8885-8886`).
- The newest edition (the DOCX capture) omits it at SD:4579 and states the general rule at SD:3856 ("You could do a WRPIN while DIR is high, but the unregulated change in use of the 126 state bits would cause unpredictable and quite certainly useless behavior"). That rule's own reasoning is about changing the five `%SSSSS` mode bits; a sniffer toggle keeps `%11011` selected (SD:3856 "multiplexes those 126 bits to the … subcircuit selected by the five %SSSSS mode bits"). That is an inference, so it does not close the row.
- Separate and documented: **WXPIN** settings (host/device D[15], full/low speed D[14], baud) "can be changed on-the-fly without resetting the USB smart pins", SD:4581, "necessary when talking to both 'full-speed' and 'low-speed' devices over a USB hub".
- HDL (indicator): no sniffer text (`sniff` returns nothing); `aspects/MODE-SWITCH-INHERITANCE.md:327` lists what the even USB pin's reset reaches, not a same-mode WRPIN.
- Search record: `new WRPIN`, `without resetting`, `sniffer` in SD, HW, TI, `p2-documentation.txt`, KB, EF, VO; control hit HW:1488.

Correction to the bench question already filed (S-324, "does a new WRPIN with DIR high switch **host ↔ device** without a DIR cycle", `VO-F372`): host/device is a WXPIN field and SD:4581 already says it can change live. The WRPIN sentence concerns the **drive/sniffer** change (`%1_11011_0` ↔ `%0_11011_0`). Reword VO-F372 to that.

**VO-F372 (reworded).** USB pair P0/P1 (even/odd) running as device or host with a packet sendable (WYPIN `$80`, bytes, IN on the odd pin); a second USB pair P2/P3 configured `%0_11011_0` as a sniffer, jumpered P0→P2, P1→P3 (all within the free pins P0–P7). Arms, each with a control: (1) drive: send a packet from P0/P1, the sniffer receives it; (2) with DIR still high, WRPIN P0 and P1 to `%0_11011_0`: send again; expect the sniffer sees nothing and P0/P1 stay running (no reset), (3) WRPIN back to `%1_11011_0` with DIR still high, send again; (4) the same sequence with a DIR cycle between each WRPIN as the control. Verdict: survives (HW/TI/old SD right; add the exception) or breaks (SD v35 right; delete the sentence). **Jumper-testable on free pins P0–P7.**

KB change: `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml:17-29` (`wrpin_data_conflict`) says "No document separates the two; they are the same document." Replace with: three documents carry the sentence (HW:1488, TI:1382, older P2 Documentation), the newest edition omits it, bench pending. Keep `:16` as is until the bench.

Cross-reference: S-324 / VO-F372, F-372.

---

## G-028 — PASM2 / hardware call stack, 9th push

**Unknown:** what the 8-level hardware stack does on a 9th push.

**State: BENCH QUESTION (every source silent). Pure silicon, no pins.**

Search (terms; files; control): `8-level`, `eight-level`, `hardware stack`, `stack depth`, `ninth|9th`, `overflow`, `wrap`, `overwrit`, `oldest`, `circular`, `deeper`, `nest` in SD, DS, HW, PM, CSV, EF, VO, spin2-v55, `Spin2_interpreter.spin2` (v55), `Spin2_debugger.spin2` (v51), HDL (`-w stack`, `stk`, `eight-level`), `pnut_ts_facts/SingleStep-Debugger-Theory-of-Operations.md`, the Silicon Doc review comments. Control hit: SD:166, SD:866, PM:776 ("The 8-level hardware stack"), PM:5788-5791 (POP/PUSH).
What exists, all short of the question:
- Depth only: SD:166, DS:75, PM:776.
- Under-run is defined and over-run is not: SD:1149-1150 `rep @.r,#8` / `push ##byteloop '(bottom stack value gets copied each _RET_ / RET)`; SD:866-867 `REP #1,#8 'pre-stuff 8-level hardware stack with 'loop' address` (8 pushes fill it).
- The debugger saves with exactly 8 `POP` and restores with exactly 8 `PUSH` (`Spin2_debugger.spin2:315-322`, `:400-407`): consistent with an 8-deep store, silent on a 9th.
- HDL indicator: `P2-THEORY-OF-OPERATIONS.md:2265-2266` "pushed … onto the eight-level hardware stack"; no overflow text.
- KB: `architecture/xbyte_engine.yaml:234` "Hardware stack must not overflow" and `language/pasm2/concepts/stack_operations.yaml:56-57` "depth: 8 levels" assert no behaviour; keep.

**VO-G028.** In one cog, after emptying the stack with 8 `POP`s: `PUSH #1 … PUSH #9` (nine distinct values), then 9 `POP`s into nine registers; report the nine values. Pre-registered readings: **drop-oldest** → pops 9,8,7,6,5,4,3,2 then the ninth pop equals the bottom (2); **drop-newest/overwrite-top** → pops would begin 8 (or 1) … ; **wrap/other** → anything else. Add the same with `CALL`/`RET` nested nine deep with a distinct return target each. Control: 8 pushes, 8 pops return 8..1 (must hold or RIG FAIL). Report from a cog that is not measuring (EF-057 rule). **Pure silicon, no pins; no jumper.**
Value: states, for the first time, what a ninth CALL does; twin of F-392 (Spin2 side). Search record above is the "sources silent" proof.

---

## G-029 — Lookup RAM / smart pins

**Unknown:** what "as a data source for smart pins" means for Lookup RAM.

**State: OUT OF REACH (a designer's statement; no source and no testable mechanism is named).**

Evidence: the phrase is at SD:476, DS:599, HW:379 and nowhere explained. The only LUT-to-pins paths the sources describe are the streamer's: SD:159 "stream hub RAM and/or lookup RAM to DACs and pins", SD:1318 "Immediate ⇢ LUT ⇢ Pins/DACs", SD:1340 "RDFAST ⇢ LUT ⇢ Pins/DACs", SD:500 "The 2nd port is also shared by the streamer in DDS/LUT modes". Reading "smart-pin data source" as "the streamer, whose output goes to pins/DACs" is inference and does not close the row. Searched `(lut|lookup)` within 80 characters of `smart|wxpin|wypin|wrpin` (and the reverse) in SD, HW, DS, HDL, `pnut_ts_facts`, EF: no mechanism; HDL has only the unrelated `SO12` lookup. VO-J-006 (LUT sharing) is a different mechanism (paired-cog `SETLUTS`), so it does not answer this. No bench can be written until a mechanism is named.

Proposed: **Q-011** to Chip Gracey (see below). KB: nothing stated, correctly.

---

## Proposed KNOWLEDGE-GAPS.md updates (the arbiter applies them)

Next IDs are currently `G-030` / `Q-010`; this proposal uses Q-010 and Q-011, so the "Next expert-question ID" becomes `Q-012`.

| Gap | Status move | "Filled by (source @ edition)" text to record |
|---|---|---|
| G-002 | OPEN/PARTIAL stays PARTIAL | Cadence: SD:3934-3959, HW:1080-1094 (already recorded). ENOB → Q-008, no change. |
| G-004 | PARTIAL → **ANSWERED (timing)**; example half → closed as "no source holds one; KB example unsourced, defects tracked S-003/S-230/S-300 + new `:16` base-period wording" | SD:4078-4090 @ v35 DOCX; HW:1156-1165 @ 2022/11/01 |
| G-005 | PARTIAL → **ANSWERED (scope + sysclk < 1/4)**; the FS > 80 MHz claim stays only as Q-003 | SD:4577-4593, HW:1487-1489 |
| G-006 | OPEN → **ANSWERED (%00110 Y=0)**; add: `%00111` Y=0 and interval jitter open as VO-G006a/VO-G006b | **EF-013** (bench, 2026-06-17, iosp-titus-verification-batch1 RA-12) |
| G-009 | OPEN → **ANSWERED** | 64004-ES Product Guide v1.0 11/5/2019, p.7, read from the rendered page 2026-10-09: HyperRAM `IS66WVH16M8BLL-100B1LI`; HyperFlash `IS26KL256S-DABLI00` (letter I, not digit 1). The OCR copy's `DABLl00` and `issi.c0m` are OCR errors. ISSI datasheets not cross-checked. |
| G-012 | OPEN → **ANSWERED** (convention read from figures) | 64004-ES Product Guide p.3/p.8 + schematic J100/J101 `IO+0…15`; Eval Board guide p.17 header silkscreen. |
| G-015 | PARTIAL → stays PARTIAL; reword | Held: none committed. Outstanding: #64009 microSD and #64010 motor-driver archives (not held); staged-uncommitted RTC/HD-Audio/WX archives await a code-pass ingestion. |
| G-019 | OPEN stays; add | 2026-10-09 re-search: no P2 pin AC figure in any source; two derived notes (`p2-complete-signal-flow-matrix.md:155`, `p2-addon-board-circuit-knowledge.md:395`) are not sources. |
| G-020 | OPEN → **PARTIAL**; correct the row text | DS:331-333 states bypass caps close to every VDD/Vxxyy and a GND pad tied to a solid ground plane with multiple vias; still absent: θJA, derating, EMC. `p2-board-power-analysis-matrix.md:143` θJA is not a source. |
| G-022 | OPEN stays; add routing | New **Q-010**: mikroBUS spec (document not held). |
| G-023 | OPEN → **ANSWERED (low)**; retitle the row from `%10xxx counting` to `%01010 SMPS` | SD:4080 and :4090, HW:1157; HDL indicator `SMART-PIN-MODULATION-ENGINE.md:277`. |
| G-024 | OPEN → **ANSWERED/CLOSED for the KB** | PM:3762/3806/3830 and SD:669 "at least two instructions" (KB carries it); the reviewer's mechanism stays an upstream lead (forum thread not fetched). Optional VO-G024. |
| G-025 | OPEN → **ANSWERED** | CSV row 44; SD:60; PM:1064, :1501-1503. Not a BITC defect: S[9:5] is the span field. KB follow-up: span rule missing from `bitc/bitnc/bith/bitl/bitz/bitnz.yaml`. |
| G-027 | OPEN stays (bench) | Correct "no second source": HW:1488, TI:1382, `p2-documentation.txt:8885-8886` carry the sentence; SD:4579 (newest) omits it; WXPIN live-change is separate and documented at SD:4581. Bench = VO-F372, reworded to the sniffer/drive change. |
| G-028 | OPEN → stays OPEN with a bench question | New **VO-G028** (pure silicon). |
| G-029 | OPEN → **STILL-UNKNOWN**, escalate | New **Q-011**: "What does Lookup RAM's 'data source for smart pins' refer to — which instruction or mode reads the LUT?" Who: Chip Gracey. Links: G-029, SD:476, DS:599, HW:379. |

New Part B rows:

| Q-010 | What do the mikroBUS socket nets `TX` and `RX` denote — the host's or the Click module's UART pin — and are the B-header rails `5V_B`/`VIO_3V3_B` commoned with `_A`? | The 64008 Rev A schematic gives net names only (`p2-click-adapter-netlist.md:113-114`, `:164`); the MikroElektronika mikroBUS specification is not in the corpus. | MikroElektronika spec (ingest it) / Parallax for the rails | open | G-022 |
| Q-011 | What does "Lookup RAM as a data source for smart pins" mean: which smart-pin mode or instruction reads the LUT? | Stated in three sources (SD:476, DS:599, HW:379), explained in none; the streamer's LUT-to-pins paths (SD:1318, :1340) are a different mechanism until the designer says otherwise. | Chip Gracey | open | G-029 |

---

## Defects seen while reading (outside the 16 gaps)

- `smart-pin-01010-pwm-smps.yaml:16,23` "System clock ÷ X[15:0]" / "divisor" contradicts SD:4074 (G-004, new; not on the study).
- `addon-hyperram-hyperflash.yaml:153` wrong part-number string (G-009).
- `smart-pin-11011-usb-host-device.yaml:17-29` states a false premise ("same document"; G-027).
- Ingested OCR text `sources/hyperRam-n-hyperFlash/hyperram-hyperflash-text.txt:153,155` carries two OCR errors: a finding for the ingestion head, not edited.
- Gap rows G-020 and G-027 contain statements the sources contradict (corrected above).

## Not checked

- Eval Board guide p.17 (P0–P7 silkscreen) and each add-on's own silkscreen beyond HyperRAM, for G-012.
- The ISSI datasheets themselves (G-009).
- The older `smart-pins/` and `central-analysis/` 2025 notes (stale; superseded by this ledger) and the OBEX example corpus for SMPS/USB use beyond a string search.
- Compiler probes: none run; no gap here is a legality question.
