# Silicon Doc walk, range 7: SD:4254-4818 (remaining smart pin modes, boot process)

KB root below: `deliverables/ai/P2/`. Smart-pin pages abbreviated `sp-NNNNN` =
`architecture/smart-pins/smart-pin-NNNNN-*.yaml`; `smart_pins` = `architecture/smart_pins.yaml`.

## Sections

| SD line | Heading | Disposition |
|---|---|---|
| 4254 | (tail of %10111: "During reset IN low, Z=$0") | Belongs to range 6; IN-PLAN §7 reset table. |
| 4257 | %11000 / %11001 ADC sample/filter/capture | Carried on sp-11000 and sp-11001, unevenly: sp-11001 carries the WYPIN override, 27-bit limits and settling; sp-11000 (the internal-ADC page agents read first) says Y is unused and lacks them. Table 34 not carried as a table. |
| 4392 | About SINC2 and SINC3 filtering | Partly carried (sp-11001 notes); settling and prescale/post-trim missing from sp-11000. |
| 4414 | SINC2 Sampling Mode (%00) | MATCH. |
| 4431 | SINC2 Filtering Mode (%01) | Carried, but sp-11000's example drops the ZEROX trim. |
| 4460 | SINC3 Filtering Mode (%10) | Shift rule carried only on sp-11001, and only as a comment. |
| 4492 | Bitstream Capturing Mode (%11) | Mostly carried; "captures A regardless of pin config" not carried. |
| 4509 | %11010 ADC Scope with Trigger | Carried well (A/B, filter select, arming table, C=armed). Two unsourced/wrong lines. |
| 4551 | SCOPE Data Pipe | SETSCP/GETSCP pages carry the bits; pipe purpose and time alignment thinly carried. |
| 4577 | %11011 USB | Mostly carried (status word verbatim, WXPIN bits, WYPIN codes). Upper-pin IN wording wrong, IDLE wrong for host, upper-pin acknowledge rules, bit-period sync, end-of-packet detection, byte-toggle idiom not carried; examples do not compile. |
| 4640 | %11100 sync serial transmit | Carried; hold-time line mis-tied to X[5]=1; reset output state not carried. |
| 4663 | %11101 sync serial receive | MATCH on the substance. Internal inconsistencies in its own examples. |
| 4684 | %11110 async serial transmit | IN wording and buffering IN-PLAN §1/§7. Fraction condition, reset output, busy-poll timing not carried; one example computes a garbage bit period. |
| 4717 | %11111 async serial receive | Stop bit IN-PLAN §1. Fraction condition not carried. |
| 4741 | BOOT PROCESS (needs more editing) | Table 36-38 MATCH `boot-pattern-selection.yaml`. Booter prose: hub copy of first 1 KB not carried; SD prose's own P60 fast-boot step contradicts SD Table 36 (source issue, KB follows the table). |

## Ledger

| SD lines | Fact (one line) | C/M | YAML home (file:line) or NOT-CARRIED | Disposition | Note (quotes, searches) |
|---|---|---|---|---|---|
| 4262 | Internal ADC: A sampled every clock; A must be in ADC pin mode M[12:10]=%100 | C | sp-11000:12, :169 | MATCH | "Requires M[12:10] = %100 in WRPIN configuration to enable ADC" |
| 4262 | External mode: A sampled on each B rise (external delta-sigma) | C | sp-11001:10, :16 | MATCH | "A-input sampled on each B-input rising edge" |
| 4264 | Period = 2^X[3:0]; X[5:4] picks mode | C | sp-11001:30; sp-11000:30; smart_pins:540 | PARTIAL | sp-11001 "Sample period = 2^(X[3:0]) clocks"; sp-11000 only "Sample period configuration (resolution/period setting)", no formula. |
| 4267-4385 | Table 34: resolution/ENOB per period per mode, and where each mode overflows | C | sp-11001:157-167 (excerpt) | PARTIAL | sp-11001 lists 3 SINC2-sampling, 3 SINC3, 1 bitstream rows, all matching (e.g. "128 clocks = 14 bits", "8,192 clocks = 14 bits"). The overflow boundaries (SINC2 sampling at %1110+, SINC3 at %1010+, bitstream at %0110+) and the %0000 impractical row are not stated. Searched `overflow`, `impractical`, `16,384`. |
| 4385 | ENOB column defined as "Effective Number of Bits, or the sample resolution"; SINC3 "doubles the ENOB ... for fast signals" (4396) | C | sp-11001:162, :180-181 | MISMATCH | KB: "NOMINAL decimation word-width (bits), NOT measured ENOB" and "The SINC3 column's apparent doubling ... is an idealized figure the P2 ADC does not actually deliver". No source cited for either sentence; ledger has no ENOB EF (grep `ENOB` in P2-EMPIRICAL-FINDINGS.md: 0). |
| 4387 | Modes > %00: WYPIN after WXPIN overrides period with Y[13:0] | C | sp-11001:32, :172; smart_pins:540; **sp-11000:32** | MISMATCH | sp-11000:32 `y_register: function: "Not used in this mode"`. sp-11001 right: "Optional override for sample period". smart_pins:627 `adc_11000_11001: wypin: "Not typically used"` (vague). |
| 4387 | Accumulators 27 bits; SINC3 up to 512 clocks/period, SINC2 filtering up to 11,585 | C | sp-11001:174-176; P2AN001:105 | PARTIAL | Carried on sp-11001 ("SINC3 limited to 512", "SINC2 supports up to 11,585") but absent from sp-11000 (grep `27`, `11,585`, `512` on that file: none). |
| 4389 | End of period: measurement to Z, IN raised, new measurement begins | C | sp-11000:19, :37; sp-11001:19-20 | MATCH | "IN flag raised when sample period completes / New measurement begins automatically" |
| 4394 | SINC2 filtering accurate from the third sample | C | sp-11001:173 | PARTIAL | Only on sp-11001; sp-11000 none (grep `third`). |
| 4396 | SINC3 filtering accurate from the fifth sample | C | sp-11001:173 | PARTIAL | As above. |
| 4396 | SINC3 limited to 512 per period, better for dynamics; SINC2 better for DC | C | sp-11001:175 | PARTIAL | Limit carried; the DC vs dynamic guidance not. |
| 4398-4412 | 27-bit rollover: prescale SHL #5 before SUB, or ZEROX #26 after | C | sp-11001:177, :107 | PARTIAL | sp-11001 "Prescale 27-bit to 32-bit (SHL #5) or post-trim (ZEROX #26)". sp-11000 lacks it. |
| 4416 | %00 sampling: complete in hardware, power-of-2 periods only; read with RDPIN | C | sp-11000:26, :171 | MATCH | "%00 = SINC2 sampling (complete conversion in hardware, power-of-2 periods only)" |
| 4420-4421 | Setup word `%100011_0000000_00_11000_0`, `WXPIN #%00_0111` = 8 bits | C | sp-11000:63-73, :141 | MATCH | `long %0000_0000_000_100011_0000000_00_11000_0` |
| 4424 | adcpin bits 10..6 configure extra pins at once | C | sp-11000:13, :173; `language/pasm2/akpin.yaml:5` (range encoding) | PARTIAL | "Multiple consecutive pins can be configured simultaneously"; the bits-10..6 form is on the pin-instruction pages, not linked here. |
| 4441-4452 | %01 loop: SETSE1 on IN high, RDPIN, SUB/ADD diff, SHR, **ZEROX x,#7** | C | sp-11000:91-98 | MISMATCH | KB loop: `sub sample, diff` / `add diff, sample` / `shr sample, #6` / `mov outa, sample` — no ZEROX, so after a 27-bit accumulator wrap the upper bits of `sample` are garbage (SD:4398 "32-bit integer adds and subtracts ... will roll over incorrectly"). |
| 4457 | SINC2 filtering shift = LOG2(clocks)-1 | C | sp-11000:174, :97 | MATCH | "SINC2 post-processing: shift right by [LOG2(samples)]-1" |
| 4474-4489 | SINC3 loop: two diffs; shift = LOG2(clocks); trim | C | sp-11001:103-110 | PARTIAL | sp-11001 comment "shift right by LOG2(clocks per period)"; sp-11000:175 only "SINC3 requires difference calculations". |
| 4494 | Bitstream: buffers 32 bits, read every 32 clocks; bit 31 newest, bit 0 31 clocks earlier | C | sp-11000:29, :170; sp-11001:29 | PARTIAL | "LSB=oldest" matches. sp-11000:170 "provides a new 32-bit snapshot every 32 system clock periods" is true only for X[3:0]=%0101; the period field still governs IN. |
| 4506 | Bitstream mode captures the A input regardless of pin configuration | C | NOT-CARRIED | NOT-CARRIED | grep `without regard`, `regardless`, `any pin`, `digital capture` in smart-pins: none. Home: sp-11000 x_register %11. |
| 4511 | Scope: 8-bit sample + hysteretic trigger every clock | C | sp-11010:17-18 | MATCH | "On every clock the mode computes an 8-bit ADC sample and checks hysteretic triggering" |
| 4513 | Three windowed filters; 8-bit normalized, DC range ~5-6 bits | C | sp-11010:27, :137 | MATCH | "effective DC dynamic range is only ~5-6 bits" |
| 4513 | Filter shape plots | M | NOT-CARRIED | NOT-CARRIED | Mechanism; brief. |
| 4515-4533 | A/B 6-bit MSB-justified; Table 35 arming/trigger pattern | C | sp-11010:25-31 | MATCH | "A>B: arm when sample[7:2] >= A, then trigger when sample[7:2] < B" |
| 4538-4545 | X[15:10]=B, X[7:2]=A, X[1:0] filter (%00 68 Tukey, %01 45 Tukey, %1x 28 Hann) | C | sp-11010:25-27 | MATCH | Verbatim in meaning. |
| 4546-4548 | RDPIN/RQPIN: 8-bit sample, armed in C; IN on trigger cancels armed | C | sp-11010:35, :38 | MATCH | "C flag returns the 'armed' state" |
| 4536-4548 | Scope uses X only; B *input* has no stated role | C | sp-11010:40 | MISMATCH (unsourced) | KB `b_input: "Optional external trigger or clock"`. SD's A and B here are X fields, not pin inputs; no source gives the B input a role in %11010. |
| 4546 | (TESTP reads IN, not armed) | C | sp-11010:71 | MISMATCH (comment) | `testp #adc_pin wc ' Check for trigger (C = armed)`; TESTP returns IN; armed comes only from RDPIN/RQPIN WC (SD:4546). |
| 4553 | Each cog's SCOPE pipe carries lower bytes of RDPIN values of a 4-pin block, time-aligned, so the streamer can record four 8-bit samples per clock | C | sp-11010:142; getscp:12 | PARTIAL | sp-11010 "can aggregate four 4-pin-block samples per clock for the streamer" (garbled: one block of four pins). Streamer side not linked (grep `scope` in `architecture/streamer/`: no pipe hit). |
| 4557 | SETSCP D[6] enable, D[5:2] selects 4-pin block | C | `language/pasm2/setscp.yaml:12` | PARTIAL | "set input pin base to D[5:2]" — reads as a pin number; D[5:2] is a block number (pins 4·D[5:2]..+3). |
| 4561-4572 | GETSCP bytes: pin3 in [31:24] .. pin0 in [7:0] | C | `language/pasm2/getscp.yaml:12` | MATCH | "D = {ch3[7:0],ch2[7:0],ch1[7:0],ch0[7:0]}" |
| 4574 | Pipe generic: carries any RDPIN low bytes | C | NOT-CARRIED | NOT-CARRIED | grep `generic`, `SCOPE data pipe` beyond sp-11010:142: none. Home: getscp.yaml. Low consequence. |
| 4579 | USB: even/odd pair, OUT and HHH_LLL overridden; lower=DM, upper=DP; one WRPIN `%1_11011_0`; `%0_11011_0` = sniffer; FPGA has no resistors | C | sp-11011:14-20, :42 | MATCH | Verbatim. |
| 4581 | WXPIN on lower pin sets mode/baud; changeable on the fly | C | sp-11011:29-38 | MATCH | Plus EF-102. |
| 4583 | D[15] host/device affects only IDLE drive: host = both pins 15k pull-down; device = one pin 1.5k pull-up, other floats, D[14] picks which | C | sp-11011:29, :49 | PARTIAL | "D[15] must be 1 for 'host' or 0 for 'device'". The IDLE resistor behaviour is quoted only in `pin-drive-configuration.yaml:20` and `basic-io.yaml:178` as a drive-ladder example, not on the USB page. |
| 4585 | D[14] FS idle = DM low/DP high; LS opposite; DP/DM swappable by swapping speed | C | sp-11011:18, :50 | PARTIAL | Swap caveat carried; the idle levels per speed not (grep `idle state`, `DM low`: none). |
| 4587 | Baud = 16-bit fraction of sysclk, two MSBs 0 (< sysclk/4); 80 MHz example $2666; host+FS = $C000\|$2666 | C | sp-11011:29, :39, :51-52 | MATCH | `WXPIN ##$E666` = $C000\|$2666 (SD's own "WXPN" is a typo). |
| 4589 | Upper pin IN high whenever the **two-level FIFO** has room for another byte | C | sp-11011:16, :78 | MISMATCH | KB: "IN is raised whenever the output buffer empties". Room for one byte in a two-level FIFO is not "empties". grep `two-level`, `room for`: none. |
| 4589 | WXPIN/WYPIN on the upper pin act as AKPIN; AKPIN on upper pin needed to see next not-full | C | sp-11011:16, :78 | NOT-CARRIED | KB says only "No WXPIN/WYPIN instructions are used for this pin." grep `acknowledge` on sp-11011: none. |
| 4591 | Lower pin IN on receiver status change; RDPIN gives 16-bit status; WXPIN baud, WYPIN output | C | sp-11011:17, :79 | MATCH | |
| 4593-4595 | Start: DIR low, `WRPIN #%1_11011_0,bothpins`, WXPIN, DIR high; send with `WYPIN byte,bothpins`, which also acknowledges the upper pin | C | sp-11011:40, :62 | PARTIAL | KB: "configure them each via WRPIN ... send packets via WYPIN, both on the lower pin". The both-pins WYPIN that acknowledges the upper pin is not stated. |
| 4593 | (examples must configure both pins) | C | sp-11011:104, :125, :147 | MISMATCH (code) | All three examples WRPIN/PINSTART only `usb_dm_pin`. The Spin2 example uses undefined `x_config`, `y_config`: pnut-ts 1.55.10 `error: Expected an expression term (m172)` on line 6 of a minimal copy. PASM example sets baud 0 (`usb_config long 0`). |
| 4599 | WYPIN 0 = IDLE: two 15k pull-downs (host) or 1.5k pull-up + float (device) | C | sp-11011:56 | MISMATCH | KB `"0 = output IDLE (float pins)"`. Wrong for host mode. |
| 4600-4605 | WYPIN 1 SE0, 2 K, 3 J, 4 EOP, $80 SOP, data bytes after SOP | C | sp-11011:57-61 | MATCH | |
| 4608 | Packet: WYPIN #$80, then bytes; auto EOP; wait upper IN before each WYPIN | C | sp-11011:62 | MATCH | |
| 4610 | All output synced to the NCO baud; each state one bit period if followed, else persists | C | NOT-CARRIED | NOT-CARRIED | grep `bit period` on sp-11011: only in status bits; grep `synchron`: none. |
| 4612 | Packet done: poll RDPIN status bit 2 (SE0 in) high; then next WYPIN starts a new packet | C | NOT-CARRIED | NOT-CARRIED | grep `packet complete`, `bit 2`, `transmit.*complete` on sp-11011: none. Without it a driver cannot tell a new packet from a continuation. |
| 4614 | Separate TX/RX state machines, shared baud; receiver sees local output | C | sp-11011:41 | MATCH | |
| 4616 | RDPIN: status, error bit 6 into C; status IN practical mainly for plug-in | C | sp-11011:64, :80 | MATCH | |
| 4620-4629 | Status bit table | C | sp-11011:66-75 | MATCH | Verbatim. |
| 4632-4637 | Byte-toggle idiom: SHR #8 WC, RCL flags, TEST #%11 WC | C | NOT-CARRIED | NOT-CARRIED | grep `RCL`, `toggle bit into` on sp-11011: none. Bit 7 meaning is carried, the detection method is not. |
| 4642 | Sync TX overrides OUT | C | `sp-11100:33` | MATCH | "OUT overridden" |
| 4644 | Each bit output two clocks after a registered B rise; B[3] inverts for negative edge | C | sp-11100:55, :148 | MISMATCH | KB `hold_time: "Data stable 2+ clocks after edge when X[5]=1"`. In TX, X[5]=1 is start-stop mode; the 2-clock figure applies in every TX mode (the "2 clocks" belongs to RX X[5]=1's rationale, SD:4673). Negative edge carried (:55). |
| 4644 | (A input not the output) | C | sp-11100:34, :51 | MISMATCH (label) | "A=data output"; `data_pin: "Outputs serial data (A-input)"`. The pin output is driven; A is an input. |
| 4650 | X[5]=0 continuous: first word WYPIN in reset primes shifter; second after DIR high; IN on each advance | C | sp-11100:145; smart_pins:123 | MATCH | Plus EF-090. |
| 4652 | X[5]=1 start-stop: WYPIN before first clock goes straight to shifter; later WYPIN buffered until after last clock | C | sp-11100:147 | PARTIAL | KB "Can modify data before clock starts"; the buffered-after-first-clock rule not stated. |
| 4654 | X[4:0] = bits-1 | C | sp-11100:41 | MATCH | |
| 4656 | One-stage buffer; IN on each advance; in reset buffer flows to shifter | C | sp-11100:47, :145 | MATCH | "High when buffer empty (ready for next data)" |
| 4658 | MSB-first: SHL #32-n then REV | C | sp-11100:36, :119-120 | MATCH | |
| 4660 | In reset output held low; on release output = LSB of word written in reset | C | NOT-CARRIED | NOT-CARRIED | grep `held low`, `output is held`, `during reset` on sp-11100: none. Not the Z table of §7 (that is SD:3918-4254 Z values); this is the pin level. |
| 4665 | Sync RX: A sampled around B rise; B[3] inverts | C | sp-11101:52 | MATCH | |
| 4671-4673 | X[5]=0 sample before edge (no hold); X[5]=1 coincident, pairs with TX's 2-clock hold | C | sp-11101:41, :59-60, :181 | MATCH | "For fast P2-to-P2, requires 2-clock hold" |
| 4675 | X[4:0] = bits-1 | C | sp-11101:42 | MATCH | |
| 4677 | IN on word; data MSB-justified | C | sp-11101:46-52 | MATCH | |
| 4679-4681 | LSB-first: SHR #32-n; MSB-first: REV + ZEROX | C | sp-11101:36-37, :140-142 | MATCH | |
| (own) | sp-11101's examples break its own clock-routing rule | C | sp-11101:113, :168 | MISMATCH (internal) | `sync_rx_neg LONG P_SYNC_RX \| P_INVERT_B` and `WRPIN ##P_SYNC_RX, pin` carry no B routing, which the same page's critical_requirements calls "WRONG". Not an SD contradiction; seen-wrong per the KB carve-out. |
| 4686-4688 | Async TX overrides OUT; start low, stop high; 1-32 bits | C | sp-11110:10-12 | MATCH | |
| 4692 | X[31:16] whole clocks; X[15:10] fraction **only when X[31:26]=0**; value = (clocks·$1_0000) & $FFFFFC00 | C | sp-11110:24-25, :182; sp-11111:24-25, :197 | PARTIAL | Formula carried. The condition "in case X.[31..26] is zero" (bit periods of 1024 clocks or more lose the fraction) not stated; grep `31:26`, `31..26`: none. |
| 4692 | (example arithmetic) | C | sp-11110:118 | MISMATCH (code) | `bit_period := (_clkfreq * 65536) / baud` overflows 32 bits. pnut-ts 1.55.10 folds the same expression to `$FFFFDCBB` (-9029). SD defines the value from *clocks* (clkfreq/baud) times $1_0000. |
| 4694 | X[4:0] bits-1 | C | sp-11110:27 | MATCH | |
| 4696-4705 | One-word buffer ahead of shifter; IN when word moves to shifter | C | sp-11110:20, :34 | IN-PLAN §1, §7 | Plan rows "Async TX IN" and "Async TX buffering". |
| 4707-4712 | RDPIN WC returns busy; pollable 3 clocks after WYPIN (WAITX #1 idiom) | C | NOT-CARRIED | IN-PLAN §1 (partly) | §1's truth column names "busy in C means complete"; the 3-clock poll latency and the WAITX #1 idiom are not named there. grep `busy` in smart-pins: 0. |
| 4700-4701 | (state 1 raises IN only after a WYPIN) | C | sp-11110:65, :94; sp-11111:162, :167 | UNEXPLAINED | The examples wait for IN *before the first* WYPIN. Read against SD's sequence, IN is not raised until a word is written, which would stall the first send. Not settled by any source or EF read here; recorded for planning, not chased. |
| 4714 | In reset async TX output held high | C | NOT-CARRIED | NOT-CARRIED | grep `held high`, `idle high`, `during reset` on sp-11110: none. |
| 4719-4725 | Async RX: A input; X same as TX | C | sp-11111:22-27 | PARTIAL | Same X[31:26] condition missing. |
| 4729 | RX waits for A high (idle) before looking for a start edge | C | NOT-CARRIED | NOT-CARRIED | KB: "Monitors input for start bit (high-to-low transition)". A line held low never yields a word until it idles high. grep `idle`: none. |
| 4731-4734 | Half-bit check rejects false starts; data sampled mid-bit | C | sp-11111:12, :18, :212 | PARTIAL | "samples data bits at mid-bit timing"; the false-start re-check (state 4) not stated. |
| 4727-4736 | No stop-bit check | C | sp-11111:10, :13, :19, :213 | IN-PLAN §1 | |
| 4735-4738 | Shifter to Z, IN raised; MSB-justified, SHR #32-n | C | sp-11111:31, :218 | MATCH | |
| 4744-4784 | Table 36 boot patterns (six rows) | C | `architecture/boot-rom/boot-pattern-selection.yaml:27-64` | MATCH | Row by row, including "built into SD card" P60 pull-up (:126-127). |
| 4788-4796 | Tables 37/38: P63 RX, P62 TX; flash CSn/CLK/DI/DO = P61/P60/P59/P58; SD CLK/CSn swapped | C | boot-pattern-selection.yaml:105; `spi-flash-boot.yaml:35-38` | MATCH | |
| 4799-4804 | Booter loads first 1 KB of SPI **into hub $00000**, sums 256 longs to "Prop" $706F7250, copies to cog $000-$0FF | C | spi-flash-boot.yaml:41-49 | PARTIAL | KB `destination: "Cog 0 register space $000..$0FF"`; that hub $00000-$003FF also holds the image is not stated. Sum and value match. |
| 4805-4806 | Prose: P60 pull-up → JMP #$000 at once | C | boot-pattern-selection.yaml:46-50 | MATCH (KB) / source conflict | SD Table 36 and the Hardware Manual give fast boot as P59 pull-down; KB follows them. The SD prose (heading "needs more editing") disagrees with its own table. SOURCE-ERRATA candidate, no KB change. |
| 4807-4812 | 100 ms serial window then JMP to SPI program; serial load → COGINIT #0,#0 | C | boot-pattern-selection.yaml:44-45; `serial_loader.yaml:35` | MATCH | |
| 4816 | Failure: slow clock to 20 kHz, stop cog 0 | C | boot-pattern-selection.yaml:91 | MATCH | "HUBSET #1 -- 'set 20KHz oscillator' -- before COGSTOP" |

## Findings

MISMATCH and NOT-CARRIED contract rows, most consequential first.

1. **sp-11000 says Y is unused (MISMATCH).** `smart-pin-11000-adc-internal-clock.yaml:32` `y_register: function: "Not used in this mode"`. SD:4387: "For modes other than SINC2 Sampling (X.[5..4] > %00), WYPIN may be used after WXPIN to override the initial period ... with the arbitrary value in Y.[13..0]." The sibling sp-11001:32 and smart_pins:540 are right; smart_pins:627 says "Not typically used". The same page also lacks the 27-bit accumulator limits (512 / 11,585), the settling rule (third and fifth sample), the SINC3 shift, and the prescale/post-trim pair, which sp-11001:173-177 carry. Searches on sp-11000: `27`, `11,585`, `third`, `fifth`, `ZEROX`, `SHL`.
2. **sp-11000's SINC2-filtering example drops the 27-bit trim (MISMATCH, code).** `smart-pin-11000-…:95-98`: `sub sample, diff` / `add diff, sample` / `shr sample, #6` / `mov outa, sample`. SD:4449-4450 follows the shift with `ZEROX x,#7`, and SD:4398 says "32-bit integer adds and subtracts in software will roll over incorrectly". Without the trim, every accumulator wrap yields a wrong sample.
3. **Async TX example computes a garbage bit period (MISMATCH, code).** `smart-pin-11110-…:118` `bit_period := (_clkfreq * 65536) / baud`. 200_000_000·65536 overflows; pnut-ts 1.55.10 folds it to `$FFFFDCBB`. SD:4692 builds the value from clocks per bit times $1_0000. The formula text at :182 and sp-11111:197 has the same overflow when evaluated in 32 bits.
4. **USB upper-pin IN wording and acknowledge rules (MISMATCH + NOT-CARRIED).** `smart-pin-11011-…:16`, `:78`: "IN is raised whenever the output buffer empties". SD:4589: "whenever the two-level FIFO output buffer ... has room for another byte". Also not carried: a WXPIN/WYPIN on the upper pin acknowledges it like AKPIN; an AKPIN on the upper pin is needed to see the next not-full; `WYPIN byte,bothpins` writes the byte and acknowledges the upper pin (SD:4589, :4595). Searches: `two-level`, `room for`, `acknowledge`, `bothpins`.
5. **USB WYPIN 0 = IDLE is not "float pins" (MISMATCH).** `smart-pin-11011-…:56` `"0 = output IDLE (float pins)"`. SD:4599: "two 15k pull-downs for 'host' or a 1.5k pull-up and a float for 'device'". With SD:4583 (D[15] affects only the IDLE drive) and SD:4585 (IDLE levels per speed), neither is on the USB page (the resistor quote sits only in `pin-drive-configuration.yaml:20`).
6. **USB end-of-packet detection not carried (NOT-CARRIED).** SD:4612: poll `RDPIN status,lowerpin` for bit 2 (SE0 in) going high; only then does the next WYPIN start a new packet rather than continue the old one. Searches on sp-11011: `packet complete`, `bit 2`, `complete`. Home: sp-11011 `y_register.packet_send`.
7. **USB examples do not work (MISMATCH, code).** `smart-pin-11011-…:104` uses undefined `x_config`, `y_config` (pnut-ts: `Expected an expression term (m172)`); all three examples configure only the DM pin, against SD:4593 "configure them both"; the PASM example's baud is 0.
8. **Sync TX hold time tied to the wrong bit (MISMATCH).** `smart-pin-11100-…:148` `"Data stable 2+ clocks after edge when X[5]=1"`. SD:4644: each bit is output two clocks after the registered B edge, in every TX mode; X[5] in TX selects continuous/start-stop (SD:4648-4652). Also `:34`, `:51` call the output pin "A-input".
9. **Async bit-period fraction only when X[31:26]=0 (NOT-CARRIED).** SD:4692, :4723: "in case X.[31..26] is zero, X.[15..10] establishes the number of fractional clocks". sp-11110:25 and sp-11111:25 state the fraction without the condition; at 1024 or more clocks per bit the fraction is ignored. Searches: `31:26`, `31..26`, `1024`.
10. **Pin level during reset for sync TX (low, then LSB of the primed word) and async TX (high) (NOT-CARRIED).** SD:4660, SD:4714. Searches: `held low`, `held high`, `during reset`, `idle high` on sp-11100, sp-11110. Next to, but outside, §7's Z-value table.
11. **Async TX busy-poll timing (partly IN-PLAN §1).** SD:4707-4712: busy can be polled from three clocks after WYPIN (`WAITX #1`). §1 names "busy in C"; the latency and idiom are not in the plan. grep `busy` in smart-pins: 0.
12. **Async RX waits for idle-high before a start edge, and re-checks the start bit at half a bit (NOT-CARRIED / PARTIAL).** SD:4729, :4732. sp-11111:12 has only "Monitors input for start bit (high-to-low transition)". Search `idle`, `false start`.
13. **USB output synchronised to the baud NCO (NOT-CARRIED).** SD:4610: J/K/IDLE take effect at the next bit period and last one bit period if followed. Search `synchron`, `bit period` on sp-11011.
14. **USB D[14] idle levels per speed (NOT-CARRIED).** SD:4585. Search `idle state`, `DM low`.
15. **USB byte-toggle detection idiom (NOT-CARRIED).** SD:4632-4637. Search `RCL`, `toggle bit into`.
16. **Scope page: unsourced B-input role and a wrong comment (MISMATCH).** `smart-pin-11010-…:40` `b_input: "Optional external trigger or clock"`: no source gives the B input a role (SD:4536-4548 put A and B in X). `:71` `testp ... wc ' Check for trigger (C = armed)`: TESTP returns IN; armed comes from RDPIN/RQPIN (SD:4546).
17. **sp-11001 relabels SD's ENOB column and claims SINC3's doubling is not delivered (MISMATCH, unsourced).** `smart-pin-11001-…:162`, `:180-181` against SD:4385 ("ENOB = Effective Number of Bits, or the sample resolution") and SD:4396 ("SINC3 doubles the ENOB ... for fast signals"). No EF for ENOB.
18. **Bitstream mode captures A regardless of pin configuration (NOT-CARRIED).** SD:4506. Searches `regardless`, `without regard`. Home: sp-11000 x_register %11.
19. **sp-11101 examples contradict their own clock-routing rule (internal).** `smart-pin-11101-…:113`, `:168` omit B routing that `:26` calls "WRONG".

Also recorded (not KB defects): the SD booter prose (SD:4805) puts fast boot on a P60 pull-up, against SD Table 36 and the Hardware Manual (P59 pull-down), which the KB follows; this is a SOURCE-ERRATA candidate. UNEXPLAINED: the async TX examples (sp-11110:65, :94; sp-11111:162, :167) wait for IN before the first WYPIN, which SD's state sequence (SD:4700-4701) does not obviously support. Recorded for planning, not chased.

## Counts

MATCH 39 (one is a KB match against an SD self-conflict) · PARTIAL 20 · MISMATCH 12 (3 code, 1 internal, 1 comment, 2 unsourced) · NOT-CARRIED 10 (1 mechanism) · IN-PLAN 3 (one partly) · UNEXPLAINED 1.
