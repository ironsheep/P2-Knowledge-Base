# Rows S-220..S-280 — change specs («#407», 2026-10-09)

Read-only research; nothing under `deliverables/ai/P2/`, `engineering/ingestion/`, the study or the register was edited.
Abbreviations: SD = `sources/silicon-doc/silicon-doc-text.txt`, v55 = `sources/spin2-v55/spin2-v55-text.txt`,
CSV = `sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv` (line numbers are **file lines**),
OPR = `sources/spin2-v55/spin2-v55-operator-reference.md`, F547 = `f547-operator-cascade-specs.md` (cited as `F547 #n`),
G1 = `rows-S001-S040-specs.md`, G2G3 = `rows-S041-S110-specs.md`, G4G5 = `rows-S111-S161-specs.md`,
G7G8 = `rows-S162-S219-specs.md`. Paths are under `deliverables/ai/P2/` unless a root is given; every line number is that of
the file as read 2026-10-09. YAML-block indentation is stripped in the snippets (re-indent to the surrounding block).

**"compiled"** = the corrected text compiled with `pnut-ts` v1.55.8 (`-q`; `-d` for DEBUG code) in the scratch tree
`/tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad/s280/` — probe sources
`probes1.py`..`probes13.py` (library `lib.py`: it **extracts the code block from the live YAML**, applies the edit, compiles; compiled
sources in `p/`, final block texts in `out_*.txt`). The probe name follows in parentheses, e.g. `(a220_01011_fix)`. Where a "bad" form is
quoted with a compiler message, the bad form was compiled too and produced it. A compile proves **legality only**; semantics are
named separately with their source. **"compile in sprint"** = prose or YAML-level text, not compiled here.
Sweeps (scratch): `sweep_dat_locals.py` (S-220), `sweep_con_pasm.py` (S-223), `sweep_modeword.py` (smart-pin mode words: bit count and
SSSSS at bits 5:1), `sweep_gate_gap.py` (S-256), plus the `grep` commands named per row.

**States.** Change spec — S-220..S-246, S-248, S-250, S-252..S-260, S-262..S-266, S-278 (44 rows).
**Pointer (already specced elsewhere, one line each)** — S-247 (= S-288), S-261 (superseded by S-350), S-267..S-275 and S-279 (F547), S-276/S-277
(done by «#405»). **Reclassified** — S-249 (the finding is wrong: the object is real; a smaller defect remains and is specced).
**Undetermined, not a bench question** — S-251, S-280 (PNut-TS punch list 7 and 8: a fact for PNut). **No bench question** in these 61
rows. **Two corrections to the study's own proposals** are in "New findings" NF-1 and NF-2 (S-255: the form is `UDEC(value)`/`SDEC(value)`,
not `DEC(value)`; S-249: the object is OBEX 4257).

---

## G9 rows (`architecture/**`)

## S-220 PASM registers named like the same listing's `main()` locals — 6 combined listings
Sites and current text (all `code_examples[0].code`; each block is `CON` + `PUB main()` + `DAT`/`org`):
`smart-pins/smart-pin-01011-quadrature-encoder.yaml:67-68` `rdpin   position, #enc_a` / `sar     position, #2` (local `position`, `:43`) ·
`smart-pin-01100-count-a-rise-b-high.yaml:62` `rdpin   count, #sig_pin` (local `count`, `:43`) ·
`smart-pin-10000-time-a-states.yaml:70-72` `rdpin   duration, #pwm_pin wc` / `if_c    mov high_time, duration` / `if_nc   mov low_time, duration` (locals `:43`) ·
`smart-pin-10001-time-a-highs.yaml:61,65,69` `mov pulse_count, #10` (declared nowhere) / `rdpin   pulse_width, #pulse_pin` / `mov     0-0, pulse_width` (local `pulse_width`, `:42`) ·
`smart-pin-11110-async-serial-transmit.yaml:73-74,78` `mov     bit_period, ##(_clkfreq / baud) << 16` / `or      bit_period, #7` / `wxpin   bit_period, #tx_pin` (local `bit_period`, `:46`) ·
`smart-pin-11111-async-serial-receive.yaml:71-72,76` same three lines for `rx_pin` (local `bit_period`, `:46`).
Error: `Undefined symbol` at the first such register — the DAT cannot see method locals `(a220_*_orig)`; declaring the DAT register under the local's
name moves the error to the `PUB` line (`Expected a unique variable name … (m242)`, per `b3-g9-defects.json` slug `dat-pasm-register-same-name-as-method-local`). **Fix: rename the PASM register** (the Spin2 half is what
readers copy) **and declare it with `res`.**
Correct (each block compiled, all other lines unchanged):
- 01011: `rdpin   position_reg, #enc_a` · `sar     position_reg, #2` and, after `jmp     #.loop`, a blank line and `position_reg    res     1` `(a220_01011_fix)` (with `if ina.[0]` for `:55`, S-350).
- 01100: `rdpin   count_reg, #sig_pin` + `count_reg       res     1` after `jmp     #.loop` `(a220_01100_fix)`.
- 10000: `rdpin   duration_reg, #pwm_pin wc` · `if_c    mov high_reg, duration_reg` · `if_nc   mov low_reg, duration_reg` + `duration_reg    res     1` / `high_reg        res     1` / `low_reg         res     1` after `jmp     #.loop` `(a220_10000_fix)`.
- 10001: `rdpin   width_reg, #pulse_pin` · `mov     0-0, width_reg` and, after `pulse_array   res     10`, `width_reg     res     1` / `pulse_count   res     1` `(a220_10001_fix)`.
- 11110: `mov     bit_clks, ##(_clkfreq / baud) << 16` · `or      bit_clks, #7` · `wxpin   bit_clks, #tx_pin` and `bit_clks res    1` after `data    long    0`; **with** S-074 (`alignl` before `data    long    0`) and S-228 (`##@message`) — full block `(a220_11110_fix)`.
- 11111: same three lines with `bit_clks`, `bit_clks res    1` after `count   long    0`; **with** S-228 (below) and S-050 (`wait_ms`, `(a050_11111_b_fix)`) — full block `(a220_11111_fix)`.
Authority: the compiler (names are one namespace per object, G2G3 S-045); v55:285/803 (inline PASM sees locals by name — same namespace).
**Class sweep** (`sweep_dat_locals.py`: every YAML scalar with a `PUB`/`PRI` signature and a `DAT` segment — a name from the signature (parameter, result, local) used as a token in the DAT segment): 8 blocks — the 6 above, plus
`language/fundamentals/variable-scoping-best-practices.yaml` `common_shadowing_scenarios[1].problematic_code` (`buffer`; S-083) and `language/spin2/concepts/object_archetypes.yaml` `archetypes[7].template` (`pin`; S-045). No other page.

## S-221 P1 counter names `cnt`, `getcnt()`
Sites: `cog_attention.yaml:384-387` (`debugging_tips[0].code`): `IF_C    WRLONG  cnt, atn_log_ptr` (`Undefined symbol`, `(a221_atn_tip_orig)`) ·
`smart-pins/smart-pin-11010-adc-scope-trigger.yaml:108`: `waitct(getcnt() + (_clkfreq / 100_000))  ' Sample rate` (`Expected an expression term (m172)`, `(a221_11010_b1_orig)`).
Correct: `cog_attention.yaml:385-388` →
```
POLLATN WC
IF_C    GETCT   ct
IF_C    WRLONG  ct, atn_log_ptr
IF_C    ADD     atn_log_ptr, #4
```
compiled `(a221_atn_tip_fix)` (GETCT without WC does not touch C, so the three `IF_C` lines see POLLATN's flag). `11010:108` → `waitct(getct() + (_clkfreq / 100_000))  ' Sample rate` — whole block compiled with `-d` `(a221_11010_b1_fix)`.
Authority: v55:547 (`GETCT() : Count`); SD:2217-2219 (`GETCT D` gets the current CT), SD:5256 (GETCT encoding), SD:55 (64-bit system counter, `GETCT WC` upper half); no `cnt` register on P2. (The `b3-g9-defects.json` locator `silicon-doc-text.txt:2015-2030` is the COG ATTENTION section, not GETCT — corrected here.)
**Class sweep** (`grep -rn -i -E "getcnt|waitcnt|\bcnt\b"` over the tree): the two sites above; `language/spin2/methods/getct.yaml:92` is S-035 (G1), `conventions/johnny-mac-documentation-style.yaml:531` is S-070 (G2G3, inside the P1 listing); `identifier-rules.yaml:171` (`cnt` as a bad abbreviation of "counter") and `spin2-pasm2-integration.yaml:300` (says P2 has no `cnt`) are correct.

## S-222 `data := REV data` — REV is binary in Spin2
Site: `smart-pins/smart-pin-11101-sync-serial-receive.yaml:101` (`spin2_complete`): `data := REV data                          ' Reverse bit order` → `Expected an expression term (m172)` `(a222_11101_orig)` (after `idx`, S-019, is declared).
Correct: `data := data REV 31                       ' Reverse bit order (x REV y reverses bits 0..y)` — block compiled with `-d` and `PUB main() | mode, data, idx` `(a222_11101_fix)`. `1 REV 31` = `$8000_0000` `(a222_rev_semantics)`, so `REV 31` is the whole-long reversal PASM's `REV D` does.
Authority: v55:448 (`x REV y`: reverse order of bits 0..y of x and zero-extend); SD:4681 (received MSB-first data: `REV D` then `ZEROX D,#N-1`).
**Class sweep** (`grep -rn -E "(:=|\(|,) *REV +[A-Za-z_#]"`, no `-i`): this line only.

## S-223 `smart_pin_patterns.yaml:36-56` — PASM straight after a `CON` block
Current (`spi_patterns.spi_full_duplex.setup`, `:37-56`): `CON` / `SPI_CLK  = 40` / `SPI_MOSI = 41` / `SPI_MISO = 42` / blank / `' Clock generator` / `wrpin   ##P_TRANSITION | P_OE, #SPI_CLK` … → `Expected a unique constant name, "#", or STRUCT (m211)` `(a223_spi_orig)`.
Correct (compiled `(a223_spi_fix)`): after the three constants add a `clk_period` constant (the block used it without defining it) and a `DAT` / `org`:
```
' Example: CLK=40, MOSI=41, MISO=42
CON
  SPI_CLK  = 40
  SPI_MOSI = 41
  SPI_MISO = 42
  clk_period = 20                    ' system clocks per clock transition (choose for the SPI clock rate wanted)

DAT
        org

' Clock generator
        wrpin   ##P_TRANSITION | P_OE, #SPI_CLK
        …unchanged to the last dirh…
```
Authority: compiler (`CON` takes constants only); the MOSI/MISO lines already carry the right clock routes (`P_MINUS1_B`, `P_MINUS2_B`: SD:3741-3743, A/B selector `x111` = pin-1, `x110` = pin-2).
**Class sweep** (`sweep_con_pasm.py`: a `CON` section followed by an instruction mnemonic from the instruction CSV): this block only (the other hit is licence prose).

## S-224 `pinstart(adc_pin, $8_C600, …)` leaves the smart pin off
Sites: `smart-pins/smart-pin-11000-adc-internal-clock.yaml:49-51` and `:119`; related text `:141`.
Current: `' Configure ADC mode: %100011 in bits 17:12, mode %11000` / `' M[12:10] = %100 enables ADC functionality` / `pinstart(adc_pin, $8_C600, %00_0111, 0)  ' 8-bit resolution` and `pinstart(adc_base + ch, $8_C600, %00_0111, 0)`.
`$8_C600` = `$0008_C600`: SSSSS (D[5:1]) = 0 → smart pin off; M[12:10] = %010 (`(a224_const)`: `P_ADC | P_ADC_1X` = `$0011_8030`, the page's own PASM literal; `$8_C600` is not).
Correct: `:49-51` →
```
' Configure ADC mode: P_ADC (mode %11000) with the 1x input range P_ADC_1X
' P_ADC_1X sets M[12:10] = %100, which enables the ADC
pinstart(adc_pin, P_ADC | P_ADC_1X, %00_0111, 0)  ' 8-bit resolution
```
`:119` → `pinstart(adc_base + ch, P_ADC | P_ADC_1X, %00_0111, 0)`; whole blocks compiled with `-d` `(a224_11000_b0_fix, a224_11000_b2_fix)`.
`:141` `required_pin_config: "%100011_00000000_00_11000_0 (M[12:10]=%100 enables ADC)"` has 22 bits (eight zeros); the WRPIN D layout is `AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0` (SD:3731) and the silicon-doc literal has seven: → `required_pin_config: "%100011_0000000_00_11000_0 = P_ADC_1X | P_ADC (M[12:10]=%100 enables ADC)"`.
Authority: v55:1469 (`P_ADC_1X` = `%0000_0000_000_1000110000000_00_00000_0`), :1554 (`P_ADC`), SD:4420 (`WRPIN ##%100011_0000000_00_11000_0`), SD:3731/:3807 (SSSSS at 5:1, `11000` = ADC internally clocked).
**Class sweep** (`grep -rn -E "17:12|100011|8_C600|8C600"` and `sweep_modeword.py`): the sites above, plus **new sites with the same fault class** in `smart-pin-11001…yaml` (NF-3) and `smart-pin-11010…yaml` (NF-4).

## S-225 pulse/cycle X halves swapped
Sites (`smart-pins/smart-pin-00100-pulse-cycle-output.yaml`): `:27`, `:29`, `:74`, `:85`, `:107-108`; related text `:55`, `:58`, `:158`.
Source: X[15:0] = base period, X[31:16] = compare value; the output is high while the counter (X[15:0] down to 1) is above X[31:16] (SD:3970-3972); "X[15:0]=3, X[31:16]=2 → 0-0-1" (SD:3980).
Correct:
- `:27` `- "X=$0002_0003: 3-clock period, high for 1 clock (pattern: 0-0-1)"` (was `$0003_0002`).
- `:29` `- "X=$0008_0010: 16-clock period, 50% duty (8 high, 8 low)"` (was `$0010_0008`).
- `:74` `period := $0008_0010            ' X[15:0] = 16-clock period, X[31:16] = 8: high for 8 of 16 clocks (50% duty)`.
- `:85` `pattern := $0002_0003           ' X[15:0] = 3-clock period, X[31:16] = 2: high while counter > 2`.
- `:107-108` replace `MOV   x, width              ' Base period` / `SHL   x, #16               ' X[31:16] = 0 (continuous)` by the one line `MOV   x, width              ' X[15:0] = base period; X[31:16] = 0 (continuous high)` (the `SHL` moved the width into the compare half and left a base period of 0).
- Same page, found in the same pass: `:55` `' 1ms pulse, 16 times` → `' 1000-clock pulse, 16 times` (1000 clocks is 5 µs at 200 MHz — the call passes clocks, not ms); `:58` `' 50% duty, 100 cycles` → `' 50% duty, 50 cycles` (the argument is 50); `:158` `X[31:16]=X[15:0]-1: Single clock low pulse` → `X[31:16]=X[15:0]-1: Single clock high pulse (high for 1 clock of each period)`.
Spin2 and PASM blocks compiled `(a225_00100_spin_fix, a225_00100_pasm_fix)`; the page's `square_wave` routine (`:116-129`) already has the right order (`period | (period/2 << 16)`).
**Class sweep** (`grep -rn -E "P_PULSE|X\[31:16\]"` over methods/ and concepts/): `language/spin2/methods/wxpin.yaml:94` `P_PULSE: "High time period"` is the same misreading — see NF-5 for its three wrong rows.

## S-226 NCO-duty arithmetic cannot produce the stated duty
Sites (`smart-pins/smart-pin-00111-nco-duty.yaml`): `:62`, `:70-82` (+ call `:55-56`), `:114-115`; PASM `:139` (S-228).
Source: Y is added to Z every base period (X[15:0] is the base period, a 16-bit field; X[31:16] is the initial phase), duty = Y / 2^32 (SD:4021-4029); MUL multiplies D[15:0] × S[15:0] (CSV:161); QFRAC divides {D, Q|0} by S (CSV:261).
Correct:
- `:62` `y_value := (duty_percent * $FFFFFFFF) / 100` (= 0: `$FFFFFFFF` is -1) → `y_value := duty_percent FRAC 100      ' (percent << 32) / 100` — 50/25/75 give `$8000_0000`/`$4000_0000`/`$C000_0000` (`a226_frac_probe`); `100 FRAC 100` overflows (`Division overflow` `(a226_frac_100)`), so the call is for 0..99 and `$FFFF_FFFF` is the largest Y.
- `:70-82` `servo_pulse` and `:55-56` its call: **delete** (decision D3). `period := _clkfreq / 50` (= 4,000,000) does not fit the 16-bit base period and loads a phase into X[31:16]; `($FFFFFFFF / period)` = -1 / 4,000,000 = 0, so `y_value` was 0 whatever the width.
- PASM `:112-115` `MOV   y_value, duty_pct` / `MUL   y_value, ##$28F5C29   ' × (2^32/100)` / `SHL   y_value, #2` → `QFRAC duty_pct, #100         ' {duty_pct, 32'b0} / 100 = duty_pct x 2^32 / 100` / `GETQX y_value                ' Y for duty_pct percent` (MUL used only `$5C29` of the constant `(a226_mul16)`).
Blocks compiled `(a226_00111_spin_fix, a226_00111_pasm_fix)` (the PASM block also needs `WXPIN ##1000, pin` at `:126` — S-167, applied in the probe; the original fails m130 `(a226_00111_pasm_orig)`).

## S-227 `receive_msb` always returns 0
Site: `smart-pins/smart-pin-11101-sync-serial-receive.yaml:136-140` (`pasm2_complete`): `CALL  #receive_byte` (which already `SHR data,#24`) / `REV   data` / `ZEROX data, #7`.
Correct (compiled `(a227_11101_fix)`):
```
receive_msb
        MOV   pin, rx_pin
.wait   TESTP pin WC                ' Test IN flag
  IF_NC JMP   #.wait                ' Wait for data
        RDPIN data, pin             ' Read the raw MSB-justified word
        REV   data                  ' Reverse the whole long
        ZEROX data, #7              ' Keep the 8-bit word
        RET
```
Authority: SD:4677-4681 ("The data read will be MSB-justified … if MSB-first … it will need to be reversed and possibly masked … 'REV D' + 'ZEROX D,#8'" for a 9-bit word → `#7` for 8 bits); the page's Spin2 `receive_msb_first` already reverses the raw word first.

## S-228 `mov ptra, ##label` in cog-mode DAT loads a COG address
Sites: `smart-pin-11110-async-serial-transmit.yaml:82`; `smart-pin-11111-async-serial-receive.yaml:80`, `:89`, `:97`; `smart-pin-00010-dac-16bit-pseudo-random-dither.yaml:130`; `smart-pin-00111-nco-duty.yaml:139`.
Current → correct:
- `11110:82` `mov     ptra, ##message` → `mov     ptra, ##@message` (the two builds differ by one byte: `20` = cog register of `message` vs `96` = its hub address, `cmp -l` of `(a220_11110_fix)` and `(a228_11110_nohub)`).
- `11111:80` `mov     ptra, ##buffer` → `mov     ptra, ##@buffer`; `:89` `cmp     count, #buffer_size wz` → `cmp     count, buffer_size wz` (a register compare with the stored 256; `#buffer_size` was the label's cog address); `:97` `buffer  long    0[256]                     ' 256-byte buffer` (256 longs = 1,024 bytes of cog image) → `buffer  byte    0[256]                     ' 256-byte buffer` `(a220_11111_fix)`.
- `00010:130` `.loop   MOV   ptra, #sine_table` → `.loop   MOV   ptra, ##@sine_table` `(a228_00010_fix)`.
- `00111:139` `.loop   MOV   ptra, #breath_table` → `.loop   MOV   ptra, ##@breath_table` `(a226_00111_pasm_fix)`.
Authority: v55:311, :320 (`#IncPins` is the cog address, `@IncPins` the hub address); G2G3 S-042 (same rule, `##@hubData`).
**Class sweep** (`grep -rn -i -E "mov +ptr[ab] *, *##?[A-Za-z_@]"`): the 5 lines above; `special-registers.yaml:158,180` (`##hub_addr`), `setq_block_ops.yaml:95` (`##sine_table_hub`), `stack_operations.yaml:92,105,214` (`##stack_base/top`) and `ptra-register.yaml:54` (`##hub_buffer`) use undeclared placeholder names — inspected, no defect asserted (the gate's `assumes` list decides). A cog-RAM label used as an immediate in a compare (`#buffer_size`) cannot be found by regexp.

## S-229 `QDIV divisor, dividend_low` — operands swapped
Site: `cordic.yaml:159` (`programming_patterns.divide_64_32.code`): `QDIV    divisor, dividend_low`.
Correct: `QDIV    dividend_low, divisor` `(a229_cordic_fix)` (D is the low dividend long, S the divisor).
Authority: CSV:260 (`QDIV`: "unsigned division of {SETQ value or 32'b0, D} / S"); `language/pasm2/qdiv.yaml:68` already has `QDIV    dividend_low, divisor`.
**Class sweep** (`grep -rn -i -E "^\s*(if_\w+\s+)?q(div|frac)\s+"`): the `qdiv clkf, #10` lines (smart-pin-01101/10010/10101/10110), `hubset.yaml:73`, `smart_pin_patterns.yaml:124`, `qfrac` lines — all put the dividend in D. This site only.

## S-230 SMPS A/B roles swapped (with S-003)
Sites: `smart-pins/smart-pin-01010-pwm-smps.yaml:59`, `:70` (and `:39`). The `dirh(…)` lines `:51`, `:56` are S-003 (G1).
Current: `mode := P_PWM_SMPS | P_OE | P_MINUS1_A | P_PLUS1_B` and `wrpin   ##P_PWM_SMPS | P_OE | P_MINUS1_A | P_PLUS1_B, #smps_out` with `v_sense = 21`, `i_sense = 19`, `smps_out = 20` → A (voltage) reads pin 19 (the current sense), B (current limit) reads pin 21.
Correct: `P_PLUS1_A | P_MINUS1_B` on both lines (A = pin 21 voltage, B = pin 19 current) — with S-003's `pinhigh(…)` the whole block compiled `(a230_01010_fix)`; the original fails at `dirh(` `(a230_01010_orig)`.
`:39` `description: "100kHz switching, voltage/current feedback on adjacent pins"` → `description: "6400-clock frame (25-clock base x 256; 39 kHz at 250 MHz), voltage/current feedback on adjacent pins"` (250 MHz / 6400 = 39.06 kHz; the example's `$0100_0019` is 256 × 25).
Authority: SD:4090-4091 (A = voltage detector, low A starts a cycle; B = over-current detector), SD:3731-3743 (A/B selectors: `x001` = pin+1, `x111` = pin-1), SD:4076/:4080 (frame, A-gated restart).

## S-231 sync-serial "companion" examples never configure the TX pin
Site: `smart-pins/smart-pin-00101-transition-output.yaml:68-77` (Spin2 `sync_serial_clock()`), `:103-118` (PASM `sync_clock`).
Current: Spin2 only `PINHIGH(TX_PIN)` (`:75`); PASM `WRPIN ##P_SYNC_TX | P_OE, pin` (`:108`) with no B route (clock = `CLK_PIN` 40, TX = 41 → pin-1).
Correct `:68-77` (compiled `(a231_00101_spin_fix)`):
```
PUB sync_serial_clock() | mode
  ' Clock for synchronous serial modes: TX_PIN is a sync-serial transmitter whose
  ' B input (the clock) is the pin one below it, CLK_PIN (P_MINUS1_B)
  PINCLEAR(TX_PIN)
  WRPIN(TX_PIN, P_SYNC_TX | P_OE | P_MINUS1_B)
  WXPIN(TX_PIN, %1_00111)         ' Start-stop, 8-bit
  PINHIGH(TX_PIN)                 ' Enable the TX data pin
  WYPIN(TX_PIN, $A5)              ' Byte to send (AFTER enable)

  mode := P_TRANSITION | P_OE
  PINCLEAR(CLK_PIN)
  WRPIN(CLK_PIN, mode)
  WXPIN(CLK_PIN, 100)             ' Bit period
  PINHIGH(CLK_PIN)                ' Enable the clock pin
  WYPIN(CLK_PIN, 16)              ' THEN trigger: 8 bits = 16 transitions
```
PASM `:108-110` → `WRPIN ##P_SYNC_TX | P_OE | P_MINUS1_B, pin   ' B input = the clock pin (pin-1)` / `WXPIN #%1_00111, pin        ' Start-stop, 8-bit` / `DIRH  pin` / `WYPIN #$A5, pin             ' Byte to send (AFTER enable)` `(a231_00101_pasm_fix)`.
Authority: SD:4644-4658 (each new bit follows a positive edge of the **B** input); the page `smart-pin-11100-sync-serial-transmit.yaml:16-31` calls the route mandatory and its example (`:61`, TX+1) is the mirror image.

## S-232 barrier of "7 signals" with seven WAITATN
Site: `cog_attention.yaml:219-236` (`programming_patterns[1]`, `broadcast_synchronization`).
Source: ATN is a single event **flag** — strobes from several cogs are OR'd, the flag is cleared by POLLATN/WAITATN/JATN/JNATN (SD:2020, :2200-2204); the page's own `limitations.no_queuing` (`:373-375`) says "Multiple signals merge into single flag". `MOV mask,#1` / `SHL mask, my_id` (`:226-227`) computed an unused mask.
Correct — replace the `code:` of the pattern (compiled `(a232_barrier_fix)`; same shape as G7G8 NF-3, which uses a lock without ATN):
```
CON
  barrier_lock   = 3           ' a number LOCKNEW returned (see locks.yaml)
  barrier_count  = $7FFF0      ' hub long, zeroed before the cogs arrive
  barrier_target = 4           ' number of cogs taking part
  group_mask     = %1111       ' one bit per participating cog (COGATN D)

DAT
        org 0
' Barrier: every cog counts itself in under the lock; the last one in
' strobes all participants, and every cog waits for that one strobe.
sync_point
        pollatn wc                          ' discard any stale attention flag first
.lock   locktry #barrier_lock wc
  if_nc jmp     #.lock
        rdlong  count, ##barrier_count
        add     count, #1
        wrlong  count, ##barrier_count
        lockrel #barrier_lock
        cmp     count, #barrier_target wz
  if_e  cogatn  #group_mask                 ' last cog in releases everyone
        waitatn                             ' returns at once if the strobe already arrived

        ' All cogs now synchronized
        ret

count   res     1
```
Authority: SD:3688 (LOCKTRY C = 1 when taken), SD:2017-2030 (COGATN mask, WAITATN), SD:2200-2204 (flag). The barrier counter must be reset before reuse (the page example is one-shot). Behaviour on silicon is **not** run here (legality only); the sequence relies only on documented flag/lock semantics.

## S-233 "owner ID is in lock_num" after LOCKTRY / LOCKRET; LOCKREL without WC tested for ownership
Sites (`architecture/locks.yaml`): `:121`, `:142-143`, `:182`.
Current: `' Lock was busy, owner ID is in lock_num` · `LOCKREL lock_num         ' Release lock` / `IF_NC   JMP #not_owner   ' Jump if we didn't own it` · `' Previous owner (if any) is returned in lock_num`.
Correct (compiled `(a233_locks_fix)`):
- `:121` → `' Lock was busy (C = 0); LOCKTRY does not write D`.
- `:141-143` → `LOCKREL lock_num         ' Release lock (only the cog that holds it can release it)` (drop the `IF_NC` line: without WC, C is not written, and with WC it reports "currently taken", not ownership).
- `:180-182` → `LOCKRET lock_num         ' Return the lock to the pool (any cog may); D is not written`.
Authority: SD:3688 (LOCKTRY: WC reports success), :3696 (only the holder can release), :3700 (LOCKREL WC: C = currently taken, a register D receives the current/last owner ID), :3686 (LOCKRET); the page itself says LOCKTRY/LOCKRET leave D alone (`:115`, `:178`).
**Class sweep** (`grep -rn -i -E "not_owner|owner ID is in|Previous owner|owner.*returned in|didn't own"`): `language/pasm2/lockrel.yaml:87` `- WC option returns previous owner` → `- WC option reports whether the lock is taken (C) and the current/last owner cog ID (a register D)`; `lockrel.yaml:66` is the **right** query form (copy of the owner, then compare) — keep; `concepts/multi_cog_synchronization.yaml:43` `with_wc: "Returns previous owner COG ID"` → `with_wc: "C = lock currently taken; a register D receives the current/last owner cog ID"`. Whether C after a self-held release reads "taken" is not stated by SD:3700 — the page must not claim either way (UNVERIFIED, not a bench candidate: the sources define the query form).

## S-234 invented "System Lock Assignments"
Site: `locks.yaml:367-373` (`debugging_tips[2].example`).
Current: `' System Lock Assignments:` / `' Lock 0: Hub mailbox system` / `' Lock 1: CORDIC engine` / `' Lock 2: Serial port A` / `' Lock 3: Shared buffer pool` / `' Locks 4-15: Available for dynamic allocation`.
Correct:
```
' Lock assignments for this project (the numbers are whatever LOCKNEW returned):
' mailbox_lock - protects the hub mailbox
' buffer_lock  - protects the shared buffer pool
' (a DEBUG build holds lock 15)
```
Authority: SD:3674-3684 (16 locks, allocated by LOCKNEW; a lock's purpose "is completely up to the application", :3682); `Spin2_debugger.spin2:77-83` (the debugger keeps lock[15] allocated); the page's own `pattern_prerequisite.lock_15` (`:92-94`). The CORDIC is not lock-based (G7G8 NF-1: overlapped commands).
**Class sweep:** `language/spin2/methods/locknew.yaml:94` `- "Consider lock assignment: Lock 0-7 for static, 8-15 for dynamic"` (invented) → `- "Document which lock number protects which resource; use the number LOCKNEW returned"`; `language/pasm2/concepts/multi_cog_synchronization.yaml:22-24` `traditional_usage: lock_15 "Reserved for debug monitor" / lock_14 "Often used for serial console" / lock_0_13 "Application-specific"` → keep `lock_15: "Held by a DEBUG build (Spin2_debugger.spin2:77-83)"`, delete `lock_14` and `lock_0_13` (no source). Lock-15 statements elsewhere (`locktry.yaml:71`, `streamer_smartpin_control.yaml:431,446`, `event_interrupt_config.yaml:300`, `multi_cog_synchronization.yaml:370`) are sourced by the debugger and stand.

## S-235 hub operations "2-9 clocks"
Site: `p2-architecture-mental-model.yaml:120-128`.
Current: `A hub operation (RDLONG, WRLONG, etc.) completes in 2-9 clocks depending on when the COG's slot arrives` and `timing: best_case: "2 clocks (slot aligned)"` / `worst_case: "9 clocks (just missed slot)"`.
Correct (compile in sprint — prose):
```
a guaranteed access slot every 8 clock cycles. A hub read (RDBYTE/RDWORD/RDLONG) takes
9...16 clocks and a hub write (WRBYTE/WRWORD/WRLONG) 3...10 clocks from cog-exec code
(9...26 and 3...20 from hub-exec code), depending on when the COG's slot arrives -- this
is deterministic and predictable, never random. For batch transfers, use
```
`timing:` → `read_cog_exec: "9...16 clocks (RDLONG)"` / `write_cog_exec: "3...10 clocks (WRLONG)"` / `batch_transfer: "1 long per clock after sync"` / `rotation_period: "8 clocks"`.
Authority: CSV:178 (RDLONG 9...16 / 9...26), CSV:247 (WRLONG 3...10 / 3...20); the KB already states it at `architecture/cog.yaml:238-239` and `guides/pasm2-getting-started.yaml:241,568` (figures for an 8-cog P2; +1 if the long crosses a hub long boundary).
**Class sweep** (`grep -rn -i -E "2-9 clocks|2 to 9 clocks|2-9 cycles"`): this page; `methods/getrnd.yaml:104` and `operators/op_rand.yaml:135` say "2-9 cycles" for GETRND/`??` (S-059/S-177 territory, unsourced). `complete-system-registers-index.yaml:316` is NF-6.

## S-236 `WRLONG value, PTRB--` "decrement then write"
Site: `system-registers/ptra-register.yaml:29`.
Current: `auto_decrement: "WRLONG value, PTRB-- (decrement by 4 then write)"`.
Correct: `auto_decrement: "WRLONG value, PTRA-- (write at PTRA, then decrement it by 4; --PTRA decrements first)"` (forms compile: `WRLONG value, PTRA--`, `WRLONG value, --PTRA` `(a236_ptr_forms)`; compile in sprint for the YAML line).
Authority: SD:3191 (`PTRA--` "use PTRA, PTRA -= SCALE"), :3195 (`--PTRA` "use PTRA - SCALE, PTRA -= SCALE"); the page's own `:49` says "PTRA-- decrements after use". The example also named PTRB on the PTRA page.

## S-237 pin ADC called "12-bit SAR, up to 1 MSPS"
Sites: `smart_pins.yaml:54`, `:496-499`, `:548` (and `:507`).
Current: `adc_per_pin: "12-bit SAR ADC"` · `adc_capabilities:` `resolution: "12 bits"` / `type: "SAR (Successive Approximation)"` / `sampling_rate: "Up to 1 MSPS"` · `filtering:` `sinc1: "First-order sinc filter"` · `adc_sample_rate: "1 MSPS maximum"`.
Correct (compile in sprint):
- `:54` `adc_per_pin: "Delta-sigma ADC with 5 ranges, 2 sources and VIO/GIO calibration; results are SINC2/SINC3-filtered bitstream sums"`.
- `:496-509` → `adc_capabilities:` `type: "Delta-sigma: the A input is sampled as a 1-bit stream on every clock (internally clocked) or on each B rise (externally clocked)"` / `modes:` `sinc2_sampling: "complete SINC2 conversion in hardware, power-of-2 periods (X[5:4] = %00)"` / `sinc2_filtering: "SINC2 accumulator, software computes the difference (%01)"` / `sinc3_filtering: "SINC3 accumulator, software computes the differences (%10)"` / `bitstream: "raw 32-bit snapshots (%11)"` / `scope: "triggered 8-bit capture (smart pin mode %11010)"`; delete `resolution`, `sampling_rate` and the `sinc1` entry (SINC1 exists only in the streamer's Goertzel mode, SD:1606-1610).
- `:548` replace `adc_sample_rate: "1 MSPS maximum"` by `adc_sample_period: "POWER(2, X[3:0]) clocks (SINC2 sampling); any period up to the 27-bit accumulator limits via WYPIN in the other modes"`.
Authority: SD:200 ("Delta-sigma ADC with 5 ranges, 2 sources, and VIO/GIO calibration"), SD:4262 (sampled on every clock), SD:4264, SD:4387 (accumulators 27 bits; 512 clocks SINC3 / 11,585 SINC2).
**Class sweep** (`grep -rn -i -E "SAR (ADC|\(Succ)|successive|12-bit|MSPS"`): `smart_pins.yaml` only (`community/obex/objects/4442.yaml:59` is an OBEX title, `8-bit SAR ADC`, correctly a software SAR).

## S-238 register totals that do not add up
Sites: `system-registers/complete-system-registers-index.yaml:23`, `:27-28`; `dira-dirb-registers.yaml:59`.
Current: `total_registers: "16 special-purpose + 8 dual-purpose + 496 general-purpose"` (= 520) · `Three per-register files exist alongside it (architecture/system-registers/ptra-register.yaml, architecture/system-registers/dira-dirb-registers.yaml)` · `set_input: "DRVL #pin_num (sets DIR bit and drives low)"`.
Correct (compile in sprint):
- `:23` `total_registers: "8 special-purpose ($1F8-$1FF) + 8 dual-purpose ($1F0-$1F7) + 496 general-purpose ($000-$1EF) = 512"`.
- `:27-28` `Two per-register files exist alongside it (…ptra-register.yaml, …dira-dirb-registers.yaml)`.
- `dira-dirb-registers.yaml:58-60` → `set_output: "DRVH #pin_num (sets DIR bit and drives high)"` / `drive_low: "DRVL #pin_num (sets DIR bit and drives low)"` / `set_input: "DIRL #pin_num (clears DIR bit: pin becomes an input)"` / `float_pin: "FLTL #pin_num (clears DIR bit, high impedance)"`.
Authority: SD:441, :444, :456 (496 + 8 + 8 = 512); CSV:397 (DRVL: OUT = 0, DIR = 1), CSV:373 (DIRL: DIR = 0), CSV:389 (FLTL: OUT = 0, DIR = 0). This page's own `memory_regions` (`:35-52`) already says 496 / 8 / 8.
**Class sweep** (`grep -rn -E "16 special|520 |Three per-register|total_registers"` and `grep -rn -E "DRVL.{0,40}(input|DIR)|set_input"`): the lines above only.

## S-239 160 MHz and 250 MHz examples against the page's own VCO limits
Sites: `clock_system.yaml:233-243`, `:245-255` (rules at `:104`, `:129`).
Current: 160 MHz — `VCO = 20MHz * 16 = 320MHz`, `Output = 320MHz / 2 = 160MHz`, words `…0000_1111_0000_1010/1011` (decoded: D=0, M=15, P=0 → VCO 320 MHz); 250 MHz — `VCO = 20MHz * 25 = 500MHz`, `Output = 500MHz / 2` (VCO 500 MHz). The page says the VCO is designed for 100-200 MHz and that overclocking to 350 MHz uses `VCO / 1` (%PPPP = 15).
Correct (both blocks compiled; HUBSET words decoded with the page's own field layout `%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS`, checked against the datasheet worked example → 148.5 MHz, `probes6.py`):
```
' 20 MHz crystal → 160 MHz via PLL
' VCO = 20 MHz * 8 = 160 MHz (inside the 100-200 MHz range); %PPPP = 15 selects VCO / 1
HUBSET  ##%10_00                              ' Enable crystal (15pF), stay on RCFAST
WAITX   ##20_000_000/100                      ' Wait 10ms
HUBSET  ##%10_10                              ' Switch to crystal (XI)
HUBSET  ##%0000_0001_0000_0000_0000_0111_1111_1010  ' PLL on, /1 * 8 / 1, source still XI
WAITX   ##20_000_000/100                      ' Wait ~10ms for crystal+PLL to stabilize
HUBSET  ##%0000_0001_0000_0000_0000_0111_1111_1011  ' Switch to PLL output
```
`(a239_160)`; and for 250 MHz: `' VCO = 20 MHz / 2 * 25 = 250 MHz, above the 100-200 MHz range (overclock); %PPPP = 15 selects VCO / 1`, words `%0000_0001_0000_0100_0001_1000_1111_1010` (`/2 * 25 / 1`) and `…_1011` `(a239_250)`. Decode: 160.0 and 250.0 MHz; the old words decode to 160/250 MHz with VCO 320/500 MHz.
Authority: `clock_system.yaml:104`, `:126-129` (the page's equations); p2-datasheet-text.txt:841-856 (worked example, PPPP = 15).

## S-240 unsourced "switching ~5 µs", "ADC clock = sysclk/2"
Sites: `clock_system.yaml:214`, `:278`.
Correct (compile in sprint): delete `:214` `switching_time: "~5 microseconds typical"` (the sourced waits are in `stabilization_timing`, `:170-177`); `:278` `adc_clock: "System clock / 2"` → `adc_clock: "Internally clocked ADC modes sample the A input on every system clock"`.
Authority: SD:4262.

## S-241 change note in served content
Site: `smart-pins/smart-pin-01110-count-a-edges-optional-b-dec.yaml:78` (last line of `configuration_order.follows_the_general_order`): `    (This page previously showed WYPIN before DIRH.)` → **delete the line.** Trivially safe.
**Class sweep** (change-note wording in the tree): scalars **served by `p2kb_get`**: `application-notes/p2an001-…yaml:93` ("CORRECTED 2026-09-09: …"), `p2an004-…yaml:90` ("previously gave"), `architecture/clock_system.yaml:177` ("An earlier form of this block …"), `architecture/smart_pins.yaml:480` ("The list previously named only…"), `architecture/locks.yaml:173-174` ("The locator previously named line 1794 … Corrected 2026-08-30, F-399"), `architecture/streamer/modes-reference.yaml:37-38`, `architecture/streamer/dds-goertzel.yaml:77`, `:316-317`, `architecture/system-registers/complete-system-registers-index.yaml:100` ("earlier text here collapsed"); YAML **comments** (not served): `hardware/hardware-compatibility-matrix.yaml:26,196,432`, `hardware/p2-hardware-selection-guide.yaml:218`, `hardware/edge-breadboard-carrier.yaml:34`, `language/spin2/methods/coginit.yaml:31`, `cogspin.yaml:28`, `architecture/lookup_ram.yaml:14`, `architecture/hub.yaml:31,250`, `architecture/streamer/pin-selection.yaml:75,230`. Decision D5 (scope).

## S-242 pin-change monitoring reads RDPIN where INA is meant
Sites (`event_system.yaml`): `:339-350` (`pin_change_notification`), `:354-370` (`synchronized_sampling`); sibling `:410` (`RDPIN   state, #BUTTON_PIN        ' Verify still pressed`).
Source: RDPIN returns smart pin n's result Z (SD:3715-3722, :3727); pin levels are INA (P31..P0) / INB (P63..P32) (SD:464-465, :1972-1973) or TESTP (CSV:365).
Correct (compiled `(a242_pinchange_fix, a242_sampling_fix, a242_debounce_fix)`):
```
' Monitor pins 7:0 for any change
MOV     last_state, INA
AND     last_state, #$FF

monitor_loop
    MOV     current, INA
    AND     current, #$FF
    CMP     current, last_state WZ      ' Z = 1 when no pin changed
    IF_NZ   CALL #pins_changed
    MOV     last_state, current
    JMP     #monitor_loop
```
(the original `XOR current, last_state WZ` also destroyed `current`, so `MOV last_state, current` stored the difference). `synchronized_sampling`: replace the three `RDPIN sampleN, #n` lines and the store by
```
    ' Sample all inputs at one instant: one MOV reads all 32 pins of a port
    MOV     sample1, INA           ' P31..P0
    MOV     sample2, INB           ' P63..P32

    ' Store samples
    WRLONG  sample1, ptr
    ADD     ptr, #4
    WRLONG  sample2, ptr
    ADD     ptr, #4
```
(three RDPINs one after another were never a simultaneous sample, and only `sample1` was stored). `:410` → `TESTP   #BUTTON_PIN WC            ' C = pin is still high (pressed)`.
**Class sweep:** `grep -rn -E "rdpin +\w+, *#[0-9]"` over `architecture/` and `language/pasm2/concepts/` — the three sites; every other RDPIN in the tree targets a configured smart pin.

## S-243 `mov dest, temp` / `add dest, #1` — the destination is not a pointer
Site: `fifo.yaml:165-173` (`sequential_read`) and, same defect, `:174-183` (`sequential_write`: `mov temp, source` / `add source, #1`).
Correct (compiled `(a243_seqread_fix, a243_seqwrite_fix)`; the originals compile `(a243_seq*_orig)` and loop on one register):
```
' Read 256 bytes from hub_buffer into COG RAM (64 longs, registers dest0..dest0+63)
        rdfast  #0, ##hub_buffer     ' Start FIFO read, unlimited blocks
        mov     idx, #0              ' index into the destination registers
        rep     @.end, #64           ' Repeat 64 times
        rflong  temp                 ' Read 4 bytes
        altd    idx, #dest0          ' next instruction's D = dest0 + idx
        mov     0-0, temp            ' Store in COG RAM
        add     idx, #1              ' Next COG location
.end
```
```
' Write COG array to Hub RAM (64 longs, registers src0..src0+63)
        wrfast  #0, ##hub_dest       ' Start FIFO write
        mov     idx, #0              ' index into the source registers
        rep     @.end, #64           ' Repeat 64 times
        alts    idx, #src0           ' next instruction's S = src0 + idx
        mov     temp, 0-0            ' Get COG value
        wflong  temp                 ' Write to FIFO
        add     idx, #1              ' Next COG location
.end
```
Authority: CSV:140 (`ALTD D,{#}S`: "Alter D field of next instruction to (D + S) & $1FF"); `ALTS` is its S-field twin.

## S-244 SINC3 post-processing has three stages and a prescale; the source has two
Site: `smart-pins/smart-pin-11001-adc-external-clock.yaml:102-112`.
Current: `shl x, #5` / `sub x, diff1` / `add diff1, x` / `sub x, diff2` / `add diff2, x` / `sub x, diff3` / `add diff3, x` / `' x now contains the sample` and `diff3   res     1` (`:119`).
Source (SD:4474-4489): `RDPIN x` / `SUB x,diff1` / `ADD diff1,x` / `SUB x,diff2` / `ADD diff2,x` / `SHR x,#7` / `ZEROX x,#13` for a 128-clock period (shift = LOG2(clocks per period)); 27-bit accumulators must be prescaled **or** post-trimmed (SD:4398-4412).
Correct (compiled `(a244_sinc3_fix)`): delete `shl x, #5`, the `diff3` pair and `diff3   res     1`, and end with
```
        sub     x, diff1                         ' First difference
        add     diff1, x                         ' Update diff1 value
        sub     x, diff2                         ' Second difference
        add     diff2, x                         ' Update diff2 value
        zerox   x, #26                           ' Trim to the 27-bit accumulator width

        ' x holds the filtered sample; for a power-of-2 period, shift right by LOG2(clocks per period) to justify it
```
(the example's 320-clock period is not a power of two, so no shift is given — the source gives none either; decision D4 offers the source's 128-clock form).
**Class sweep:** `smart-pin-11000…yaml:94-98` (SINC2) matches SD:4446-4451; no other SINC3 block.

## S-245 `JMPREL #0 ' Pipeline sync`
Site: `event_system.yaml:435` (`common_applications[2].implementation`) → **delete the line** (compiled `(a245_timeout_fix)`; `JMP #$-4` still lands on `POLLCT1`).
Authority: CSV:348 (`JMPREL {#}D`: "Jump ahead/back by D instructions"; `#0` is a 4-clock jump to the next instruction); no source gives it a synchronising role. **Class sweep:** `language/pasm2/jmprel.yaml` (instruction page) carries no such claim.

## S-246 "Y = trigger level for scope modes"
Site: `smart-pins/smart-pin-11000-adc-internal-clock.yaml:32`: `function: "Trigger level for scope modes (not used in basic ADC mode)"` → `function: "Not used in this mode"`.
Authority: SD:4538-4539 (trigger values A and B are X[7:2] and X[15:10]); `smart-pin-11010…yaml:32-33` says "Not used in this mode" and its notes `:134` say Y is not used. (`smart-pin-11001…yaml:31-32` Y = period override is right: SD:4387.)

## S-247 `WRLONG PC, trace_ptr` — answered by S-288
`architecture/debug_interrupt.yaml:213`, `:231` → `WRLONG INB, …` (the interrupted address is IRET0, which is INB inside a debug ISR): the change spec is **study row S-288** (group A table); the page's own `:272`, `:320` already use INB. Authority SD:2423, :2311, `Spin2_debugger.spin2:323`.

## S-248 modes %00010/%00011 listed only as "long repository"
Site: `smart_pins.yaml:59-62`. Correct (compile in sprint):
```
    00001: "Long repository (M[12:10] != %101) or DAC noise (M[12:10] = %101)"
    00010: "Long repository (M[12:10] != %101) or 16-bit DAC dither, pseudo-random (M[12:10] = %101)"
    00011: "Long repository (M[12:10] != %101) or 16-bit DAC dither, PWM (M[12:10] = %101)"
```
Authority: SD:3807-3813. **Class sweep** (`grep -rn -i "long repository"`): `spin2-builtin-symbols-complete.yaml:237` (P_REPOSITORY = %00001, right); `smart_pin_patterns.yaml:189` already states the `!= %101` condition.

## S-249 `isp_octoport_serial` "not in the OBEX index" — **finding overturned; one residual defect**
The object is real: OBEX **4257** "ISP high-speed 8-port serial subsystem" (Stephen M Moraco); the ingested file is `engineering/ingestion/external-inputs/source-code/obex-projects/4257-ISP_high-speed_8-port_serial_subsystem/OctoMimumFiles/OctoMimumFiles/isp_octoport_serial.spin2` (also `external-projects/P2-OctoSerial/P2-source/`), with `PUB addPort(rxp, txp, mode, baudrate, txPullup) : portHandle` (`:173`), `PUB start() : ok` (`:289`), `PUB txStr(portHandle, pStr)` (`:440`) — the page's API is right. `p2kb_obex_find "octoport"` returns 0 only because the index is keyed on the title, not the file name; the same index returns it for "octo serial". **Reclassify: unsourced → sourced.**
Residual defect found while compiling it against the real object: `multi_resource_management.yaml:106-107` pass `MODE_NONE` and `PU_3K3`, which are the **object's** constants (`isp_octoport_serial.spin2:58`, `:66`) and are undefined in the caller → `Expected an expression term (m172)` `(a249_octo_orig)`.
Correct: `serial.addPort(RX1, TX1, serial.MODE_NONE, 115200, serial.PU_3K3)` and `serial.addPort(RX2, TX2, serial.MODE_NONE, 9600, serial.PU_3K3)`; whole example compiled against the real object `(a249_octo_fix)` (with `RX1..TX2` as CON constants). Add the OBEX id where the page names the object, e.g. a `source:` line `OBEX 4257 (isp_octoport_serial.spin2)`. Authority: v55:233-236 (`object_name.constant_name`).

---

## G10 rows (`guides/`, `language/fundamentals/`, `code-examples/`, `hardware/`, `tools/`)

## S-250 `pasm-labels.yaml:46-62` — `jnz`, `cmp` without WZ, `tjz` without `#`
Current: `cmp     x, #10` / `jnz     .loop   ' Jump to local .loop` (`jnz` is not a P2 instruction: `Expected a unique name, BYTE, WORD, LONG, or assembly instruction` `(a250_labels_orig)`), `test    value, #$FF` (no WZ/WC: writes no flag), `tjz     temp, :retry` (S operand without `#` is a register address; compiles silently `(a250_tjz_nohash)`).
Correct (compiled `(a250_labels_fix)`; the `:retry` colon form is replaced because no ingested source documents it — NF-7, decision D6):
```
' Global routine
process_data
    mov     x, #0
.loop               ' Local label with dot prefix
    add     x, #1
    cmp     x, #10 wz
    if_nz   jmp #.loop   ' Jump to local .loop
    ret

' Another global routine
validate_input
    test    value, #$FF wz
    if_z    ret
.retry              ' Another local label, reused under a different global label
    rdlong  temp, ptr
    tjz     temp, #.retry  ' Jump to local .retry
    ret
```
(the probe uses `:retry`/`#:retry` too; both spellings compile — see NF-7). Authority: CSV (`TJZ D,{#}S`; conditional jumps are `IF_NZ JMP #label`); SD:3693-3694 (the documented local-label form `.try`, `IF_NC JMP #.try`).
**Class sweep:** `jnz`, `jz` as instructions — `grep -rn -E "^\s*(if_\w+\s+)?(jnz|jz|jne|jeq)\s"` returns this page only.

## S-251 symbol-length limit — **undetermined (punch list 7); counts are specced**
The limit (32 in v55:166, 30 in PNut-TS v1.55.8: `Symbol exceeds 30 characters` for CON, VAR, DAT labels, PUB names and locals alike, `(s251_*)`) is a fact for PNut (`DRAFTS/PNUT-TS-PUNCH-LIST.md` item 7). Sites that state it: 32 — `identifier-rules.yaml:15,20-21,83,176`, `pasm-labels.yaml:17`, `preprocessor/define.yaml:99`, `preprocessor/external-symbols.yaml:55,280`; 30 — `guides/spin2-getting-started.yaml:478`, `constructs/method_definition.yaml:160`, `conventions/spin2-naming-jonnymac.yaml:143,358`, `pasm2/concepts/labels.yaml:37,183`. The sprint cannot choose between them until the PNut answer. **Independent of the limit, the page's examples miscount** (lengths computed in `probes9.py`):
- `identifier-rules.yaml:67` `"this_is_exactly_32_characters_x"  # 32 chars - valid` is 31 characters; `:82-83` `this_identifier_is_way_too_long_33` is 34 ("33 chars" is wrong); `:155` `"the_current_motor_speed_value_now"  # 30 chars - too verbose` is 33.
- If PNut takes 32: `"this_is_exactly_32_characters__x"  # 32 chars - valid` and `example: "this_identifier_is_way_too_long_x"` / `reason: "Exceeds 32 character limit (33 chars)"`. If PNut stops at 30: `"this_is_exactly_30_characters_"  # 30 chars - valid`, `"this_is_exactly_31_characters_x"` / `Exceeds 30 character limit (31 chars)`, `:20` `maximum_length: 30`, and every "32" site above → 30. In both branches `:155` → `# 33 chars - too verbose`.
Lead for the check: `sources/spin2-v51/experimental-findings.md:9-12,:73-80` records `pnut_ts` v1.51.5 accepting 31-35-character symbols without truncation — v1.55.8 rejects ≥31, so the limit changed between releases (NF-8). S-147 follows this row.

## S-252 operator statements in the tutorial's `essential_operators`
Sites: `guides/spin2-getting-started.yaml:294`, `:299-300`, `:311`.
Current: `operators: "== <> < > =< =>"` · `operators: "AND OR NOT"` / `bitwise: "&& || ! (bitwise versions)"` · `post_effects: "~~ (post-set), !! (post-clear)"`.
Correct (the forms compile in a PUB `(a252_ops_ok)`; `=<` and `=>` give `Expected end of line (m281)` `(a252_bad_*)`; YAML lines compile in sprint):
- `:294` `operators: "== <> < > <= >="`
- `:299-300` `operators: "AND OR XOR NOT"` / `symbols: "&& || ^^ !! (the symbol forms of AND OR XOR NOT; logical, return 0 or -1)"` (replaces the `bitwise:` line; the real bitwise set is already at `:304`)
- `:311` `post_effects: "var~ (post-clear), var~~ (post-set), var!! (post-logical-NOT), var! (post-bitwise-NOT)"`
Authority: v55:416-420 (postfix `!!` logical-NOT, `!` bitwise-NOT, `~` clear, `~~` set), :428-429, :489-491 (`&&`/`||` are the logical AND/OR). Same as F547 #28 and G2G3 S-052.

## S-253 DITTO index given as `$`
Sites: `guides/spin2-getting-started.yaml:455`, `:460`.
Current: `- "$ (double-dollar) - iteration index within DITTO blocks"` and `LONG    $77777777 + $   ' $ is 0, 1, 2, 3` (compiles, but generates `$77777777` + the origin `(a253_ditto_dollar)`).
Correct: `- "$$ - iteration index within DITTO blocks (0 to count-1); the single $ is the origin"` and `LONG    $77777777 + $$   ' $$ is 0, 1, 2, 3` `(a253_ditto_dd)`.
Authority: v55:42 (v50: "A special index variable '$$' … iterates from 0 to count - 1 … To branch within the block, use $ (origin)"); G4G5 S-119.

## S-254 `serial.start(63, 62, 115_200)` — four arguments (with S-346)
Sites: `guides/spin2-getting-started.yaml:336` and `:397` (`serial.start(RX_PIN, TX_PIN, 115_200)`); the two convention pages are S-346 (G2G3 NF-11).
Correct: `:336` `serial.start(63, 62, %0000, 115_200)`; `:397` `serial.start(RX_PIN, TX_PIN, %0000, 115_200)` (the 3-argument call: `Expected ","` `(a254_serial3)`; the 4-argument form and `serial.str(string("Hello"))` compile against the real object `(a254_serial4, a254_pattern_fix)`; `serial.tstart(115_200)` is the object's default-pin form `(a254_tstart)`).
Authority: `jm_fullduplexserial.spin2:121` (`pub start(rxpin, txpin, mode, baud) : result`), :126-128 (`mode`: `%0xx1` invert rx, `%0x1x` invert tx, `%01xx` open-drain tx), :114-118 (`tstart(baud)`); `:263` (`str`). Note NF-9: that OBEX source does not compile unmodified under v1.55.8 (`field` is now reserved, `:403`); the probes use a scratch copy with `field` renamed.

## S-255 `DEBUG("Value: ", DEC value)`
Site: `guides/spin2-getting-started.yaml:506-507` (`debugging_support.basic_example`) and the description at `:514`.
**The study's proposed fix (`DEC(value)`) is wrong:** there is no plain `DEC` formatter — `DEC(value)` and `HEX(value)` are rejected too (`Expected an expression term (m172)` `(a255_debug_dec_paren, a255_debug_hex_paren)`). `language/spin2/statements/debug.yaml:83` states it: "There is NO plain DEC/HEX/BIN/STR/DLONG/DWORD/DBYTE -- only the U/S-prefixed numeric forms exist".
Correct: `:507` `DEBUG("Value: ", UDEC(value))` (or `SDEC(value)` for a signed value) — both compile with `-d` `(a255_debug_udec, a255_debug_sdec)`; `:514` `description: "Format specifiers (UDEC, SDEC, UHEX, UBIN, etc.)"`.
Authority: v55:947 (`UDEC(value)`), :956 (`SDEC(value)`), :1031 (the manual's own `DEBUG(UDEC(i))`). The PASM2 guide's `DEBUG("Counter: ", UDEC(count))` (`pasm2-getting-started.yaml:554`) compiles in a DAT `(a255_debug_pasm_fix)`.
**Class sweep** (`grep -rn -i -E "debug[a-z0-9_\[\]]*\(.*[ ,(](dec|hex|bin|str|dlong|dword|dbyte)[ (][a-z]"`): this line; `patterns/applications/debug_enabled.yaml:82-83` is NF-10.

## S-256 gate coverage: one-line strings under tutorial keys
The finder (`audit-kb-code-compiles.py:411-425`, `find_candidates`) passes only the **immediate** mapping key down (`walk(v, path + [kn], kn, …)`; sequence items inherit it), so a string whose nearest key is not in `_code-keys.yaml` is outside net 1, and net 2 takes only multi-line strings (`:486`). `sweep_gate_gap.py` found every string below a code-named ancestor whose own key is not code-named (about 200, mostly prose and URLs); the code-bearing ones are: `guides/spin2-getting-started.yaml:506` and `guides/pasm2-getting-started.yaml:553` (`basic_example`), `guides/pasm2-getting-started.yaml:519,523-529` (`defining_strings.syntax`/`examples.simple|multiple|with_escapes`), `language/spin2/conventions/spin2-formatting-standards.yaml` `line_length.examples.good|acceptable|poor` (holds S-346's `serial.start(RX_PIN, TX_PIN, BAUD_115200)`), `operators/op_ADDPINS.yaml` `examples[].spin2_form|pasm2_form`, and the 18 `quick_example` lines (S-137, G4G5 — found by grep because the key is not a code key).
Change spec (data, no code): add to `engineering/tools/validation/kb-compile-manifest/_code-keys.yaml` `basic_example`, `quick_example`, `good`, `acceptable`, `poor`, `spin2_form`, `pasm2_form`; restructure `pasm2-getting-started.yaml:522-529` to a list (`examples:` / `- code: |` ×3, so the existing `examples`/`code` keys apply) — generic names (`simple`, `multiple`) would also catch `identifier-rules.yaml:48` and `include.yaml:92`. Each new candidate then needs a manifest decision (≈35); `quick_example` ones fail until S-137's `'` fix is applied (`;` is `Unrecognized character`, `(n_quick_semicolon)`). The tutorials' `syntax:` notation and the 9,389 notation hits stay out (design §11 Q3). Decision D7 (recommend: adopt).

## S-257 `tools/pnut-ts-compiler.yaml` — wrong command name, quoted messages that are not the compiler's
Sites: `:7`, `:10`, `:18`, `:22-30`, `:62`, `:67`, `:73`, `:85` (key `pnut_term_ts`), `:112`, `:121` — `pnut_ts` (underscore); `:75-83` `common_errors`.
Facts (run here): the command is `pnut-ts` (`pnut-ts --help` lists `-l -v -q -o -d -F -D -I` as the page says, plus `-m -a -i -O -U -C …`); messages are `Symbol is already defined (m540)` (duplicate label), `Undefined symbol`, `Constant must be from 0 to 511 (m130)` (`#512`) `(a257_*)`; `jmp done` with no `#` **compiles** `(a257_jmp_nohash)`, so `Expected '#' or constant` is not what a missing `#` produces; none of the page's four quoted strings was found in the compiler's output. `pnut-term-ts` is not installed — its options (`-d -t -p -b -l`, default 2000000 baud) are **NOT CHECKED**.
Correct (compile in sprint): rename `pnut_ts` → `pnut-ts` on the lines above (keys `pnut_ts:` → `pnut-ts:`, `pnut_term_ts:` → `pnut-term-ts:`); **delete `common_errors` (`:75-83`)** — tool wording is not a KB fact (it drifts per release); replace the `pnut_term_ts` option tables by `run pnut-term-ts --help` (decision D8). **Class sweep** (`grep -rn "pnut_ts"`): command lines that fail when copied — `language/spin2/preprocessor/external-symbols.yaml:47-50,138,149,162,189,217-218,236,241`, `include.yaml:91-92`; prose/toolchain strings naming the tool with an underscore (≈45: the seven `application-notes/p2an00*.yaml`, `methods/cogspin.yaml:46`, `qsin.yaml:42`, `qcos.yaml:42`, `movbyts.yaml:12`, `op_swap.yaml:11,95`, `debug-mask.yaml:16,124-125`, the `debug-displays/*.yaml` `source:` lines, `code-example-schema.yaml:161`, `guides/quick-queries.yaml:34`, …) → `pnut-ts`; the ingestion directory name `pnut_ts_facts/` in source citations is a path and stays.

## S-258 add-on figures absent from the Product Guide
Sites: `hardware/addon-control-board.yaml:115-124` (`protocol_constraints`), `hardware/addon-led-matrix.yaml:104-110`, `hardware/addon-serial-host.yaml:96-106,132-161`.
Source: `p2-eval-add-on-boards-text.txt:57-88` (Control: 4 push-buttons with 470 Ω series resistors and 4 blue LEDs, "Use PWM for brightness control", :74-80), :145-197 (Matrix: ≥ 50 Hz switching, ~4 mA per LED), :99-134 (Serial Host: twin USB-A with 500 mA load switches, "such as a keyboard and mouse"). No PWM frequency, brightness-level count, debounce time, response time, 120 Hz or capability list appears there.
Correct (compile in sprint):
- Control: `protocol_constraints:` → `pwm:` / `notes: "Use PWM for LED brightness (Product Guide, p2-eval-add-on-boards-text.txt:74-80)."`; delete `recommended_frequency_hz`, `min_frequency_hz`, `max_frequency_hz`, `brightness_levels`, `notes: "Higher frequencies waste…"` and the whole `timing:` (`button_debounce_ms`, `led_response_time_ns`).
- Matrix: keep `refresh_minimum_hz: 50` and `pixel_on_time_us: "1000000 / (refresh_hz * 56)"` (56 LEDs; derived); replace `refresh_recommended_hz: 120` and `at_120hz_pixel_us: 148` by `at_50hz_pixel_us: 357  # derived: 1000000 / (50 * 56)`.
- Serial Host: delete `:132` `"USB specification compliant power management"`, `:141` `keyboard_mouse: "Standard HID devices supported"`, `:142-143` `storage_devices`/`sensors`, `:150` `"Gaming controller interfaces"`, the `storage_access` block `:157-161`, and the unsourced `use_cases` items `:99-100` (storage, sensors), `:104` (USB camera); keep "USB keyboard and mouse input".
**Class sweep** (`grep -rn -E "recommended_frequency_hz|brightness_levels|button_debounce_ms|led_response_time_ns|refresh_recommended_hz|at_120hz_pixel_us"`, and the capability phrases): these three files only; the other add-on pages' `use_cases`/`applications` blocks were not read for sourcing (NOT CHECKED).

## S-259 `edge-32mb-module.yaml:299-301` — burst formula
Current: `calculation: "((MAX_CS_LOW_USEC * (freq/1000000)) - 132) >> 4) << 4"` (unbalanced) · `typical_at_200mhz: "approximately 1280 bytes per burst"`.
Correct: `calculation: "(((MAX_CS_LOW_USEC * (freq / 1000000)) - 132) >> 4) << 4  (MAX_CS_LOW_USEC = 8, freq in Hz)"` · `typical_at_200mhz: "1456 bytes per burst (8 * 200 - 132 = 1468, rounded down to a multiple of 16)"` — arithmetic checked in `probes9.py` (1456 at 200 MHz).
Authority: `4162-MegaYume…/memstuff/psram.spin2:94` (`burst := (((MAX_CS_LOW_USEC*(freq/1000000)) - 132) >> 4) << 4`), :44 (`MAX_CS_LOW_USEC = 8`).

## S-260 five spellings "refer to the same constant"
Site: `language/fundamentals/case-sensitivity.yaml:49-50`. Correct: 
```
    - group: ["LED_PIN", "led_pin", "Led_Pin"]
      meaning: "All refer to the same constant (case is ignored; the underscore is part of the name)"

    - group: ["LedPin", "ledpin", "LEDPIN"]
      meaning: "All refer to one constant -- a different one from LED_PIN, because the underscore is part of the name"
```
`LED_PIN`/`LedPin` are two names `(a260_case_underscore)`; `LedPin`/`ledpin` and `LED_PIN`/`led_pin` are duplicates (`Expected a unique constant name … (m210)`, `a260_case_same*`). Trivially safe.

## S-261 → superseded by S-350
`code-examples/smart-pins-002-button-reading.yaml:19-24`, `:39`: `INA[BUTTON]` is a register index, not a pin bit (G4G5 NF-1); the fix is `INA.[…]`/`PINREAD(BUTTON)`, and for P32 `INB.[0]` or `PINREAD(32)`. Reclassified: spec lives in S-350 / G1 S-002 (CORRECTED note).

## S-262 "minimum 32 longs" of stack
Site: `guides/quick-queries.yaml:198` `- "Check stack size (minimum 32 longs)"`. The v55 text states no stack size (`grep -n -i stack` — none for COGSPIN); `language/spin2/methods/cogspin.yaml:73-86` already labels 32 longs "heuristic, unsourced … not a specified minimum".
Correct: `- "Check the stack passed to COGSPIN against the method's worst case (no source states a minimum; measure the high-water mark -- see language/spin2/methods/cogspin.yaml)"`. Sibling `cogspin.yaml:64` `Minimum 32 longs recommended, more for complex code.` → `Size it for the method's worst case; see stack_requirements below.` (it contradicts the page's own `:74-82`). **Class sweep** (`grep -rn -i -E "minimum (of )?[0-9]+ longs"`): these two lines. `application-notes/p2an006-sizing-cog-task-stacks.yaml` exists (cited by `cogspin.yaml:78`).

## S-263 `REPEAT idx FROM 99 TO 0 STEP -1`
Site: `guides/spin2-getting-started.yaml:261`. G2G3 S-099 settled it from the interpreter (`v55 interpreter :345-356`): the sign of STEP is ignored, direction comes from FROM/TO; both forms compile `(a263_repeat_step_neg, a263_repeat_default)`, so the line is **harmless**. Optional tidy that agrees with the tutorial's own rule at `:255-256`: `REPEAT idx FROM 99 TO 0` and `- STEP is a size; its sign is ignored (FROM/TO order determines direction)`. Authority: v55:760-763; INT:353-381.

## S-264 "local labels can shadow global labels"
Sites: `language/fundamentals/pasm-labels.yaml:77-78`; the colon form `:29-35`, `:38`, `:59-61`, `:68`, `:90-92` and `identifier-rules.yaml:133`, `:141-144`.
Correct (compile in sprint): `resolution:` → `"A local label (.name) belongs to the global label above it, so the same local name can be reused under different global labels"` and delete `conflicts:` — `.loop` under two different globals compiles `(a264_local_same_name)`, a local and a global of the same base name are distinct `(a264_local_shadow)`; nothing is shadowed. Authority: v55:813 ("regular and local symbols"), SD:3693/:4445 (`.try`, `.loop` by example) — no ingested source states a shadowing rule.
The `:name` colon spelling: accepted by pnut-ts and **the same namespace as the dot form** (`.x` and `:x` under one global → `Symbol is already defined (m540)`, `a264_dot_and_colon_same_base`; reuse under two globals compiles `a264_colon_reuse`), but **no ingested document describes it** — NF-7, decision D6.

## S-265 codenames and version stamps in served text
Sites: `guides/pasm2-getting-started.yaml:599` `(Silicon Doc v35: pipeline flush)` → `(Propeller 2 Documentation v35: pipeline flush)`; `:603` `per Silicon Doc v35 verbatim` → `per Propeller 2 Documentation v35`; `code-examples/code-example-schema.yaml:43` `examples: ["P2-Smart-Pins-Green-Book-Tutorial.md", "silicon-doc-v35-facts-only.md"]` → file names of live documents (the Green Book tutorial is retired/archived), e.g. `["engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt"]`; `smart-pins-001-basic-io.yaml:9` and `smart-pins-002-button-reading.yaml:9` `source_document: "P2-Smart-Pins-Green-Book-Tutorial.md"` → the live source of the example (decision D9: the examples need a new source or a `not-sourced` marker); the "Spin2 v51" source headers — `variable-scoping-best-practices.yaml:2`, `case-sensitivity.yaml:2`, `:26`, `identifier-rules.yaml:2`, `pasm-labels.yaml:80` → `Spin2 documentation` (no version; the KB is always latest).
**Class sweep** (`grep -rlE "Silicon Doc|Green Book|Green-Book|Blue Book"`): **≈90 files** carry "Silicon Doc" (mostly inside `source:` lines, e.g. `language/pasm2/*.yaml`, `architecture/*.yaml`) — far beyond the 10 sites O15 listed; whether the codename ban reaches `source:` citations is a decision (D9).

## S-266 `ADD x, y  WC      ' Set C if overflow`
Site: `guides/pasm2-getting-started.yaml:203`. Correct: `example: "ADD  x, y  WC      ' C = carry out of the unsigned add"`. Authority: CSV:34 (`ADD`: "C = carry of (D + S)"); the guide's own `:262`. **Class sweep** (`grep -rn -i -E "\b(add|adds|sub|cmp)\b[^'\n]*\bw[cz]+\b[^'\n]*'.*overflow"`): this line only.

---

## Operator-ingestion rows (S-267..S-280)

**S-267** invented tokens — F547 §A items 1-5 (pages `op_notandand`, `op_eqeqeq`, `op_ltshr`, `precedence.yaml:53,59`, `if_elseif_else.yaml:141-143`); re-ingestion half done by «#405» (OPR + `spin2-v55-operator-reextraction-audit.md`).
**S-268** `!`/`NOT` swap and float auto-convert — F547 #18 (float operators act on raw bits), #32 (`floating_point.yaml:73`), §E rows `op_not`/`op_adddot…`; sweep of KB pages = F547 §D/§E.
**S-269** shifted levels / missing rows — F547 §B items 6-11 (`precedence.yaml`), §C #12 (POW), §G #27 (counts).
**S-270** pages for tokens that do not exist — F547 §A #1-#4 (remove with Sacred Rule 7 redirects; decision in F547 #3).
**S-271** inherited descriptions — F547 §E table rows `op_andand`, `op_eqeq`, `op_ltgt`.
**S-272** `<<=>` — F547 §A #5 (`if_elseif_else.yaml:141-143` → `<=>`, parenthesised).
**S-273** `op_ABS.yaml:3-5` — F547 §E row `op_ABS`.
**S-274** `concepts/operators.yaml` — F547 §D items 13-23.
**S-275** `spin2-language-schema.yaml` — F547 §G #27 (17 priorities, 84 rows, drop the summary as a source).
**S-276** run-boundary spaces in `spin2-v55-text.txt` — ingestion-side, **done by the re-ingestion («#405»)** (`sources/spin2-v55/spin2-v55-operator-reference.md`); nothing in the KB tree.
**S-277** extraction audit repeats "16 levels" — **done by the re-ingestion** (audit of record `sources/spin2-v55/spin2-v55-operator-reextraction-audit.md`); the old audit is never edited.
**S-279** citations of the superseded summary — F547 §F #24 and §G #34 (`op_addmodulo.yaml:21,145`, `spin2-language-schema.yaml:19` → `sources/spin2-v55/spin2-v55-operator-reference.md`).
**S-280** `var\x` as a statement — **undetermined** (punch list 8): PNut-TS rejects the statement (`Variable needs an operator`) and accepts the term `w := v\3` (`(s280_stmt, s280_term)`); a fact for PNut. No KB page asserts the statement form today (F547 B #10 notes it open).

## S-278 citation drift (spec)
Sites: `language/spin2/operators/op_lteqgt.yaml:13` and `language/spin2/concepts/operators.yaml:329`.
Current: `in the table (:471-488).` and `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:409-491.`
Correct: `in the table (:472-488).` and `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:409-501.`
Authority (read at the lines): `spin2-v55-text.txt:409` is the table's header row, `:472-488` the comparison block (`:472` `<` … `:488` `<=>`), `:501` its last row (`TRUNC()`), `:503-505` the CON footnotes — so `:505` at `op_lteqgt.yaml:12` is right. **Class sweep** (`grep -rn -E "text\.txt:(409|410|471|472)-"`): `precedence.yaml:51` (`:472-488`, right) and the two sites; `lookup_ram.yaml:5` cites the silicon doc. Trivially safe.

---

## New findings (file:line + authority)

1. **NF-1 — the study's S-255 resolution is wrong.** `DEC(value)` does not exist; `UDEC(value)`/`SDEC(value)` do (`language/spin2/statements/debug.yaml:83`; v55:947,956; `(a255_debug_dec_paren)`). Row S-255's "the form is `DEC(value)` (m172)" and the group-G10 observation O5 must be corrected in the register. Also `guides/spin2-getting-started.yaml:514` ("DEC, HEX, BIN").
2. **NF-2 — S-249 is overturned.** `isp_octoport_serial` is OBEX 4257 (title "ISP high-speed 8-port serial subsystem"), ingested at `…/obex-projects/4257-…/isp_octoport_serial.spin2:173,289,440`; the name is absent from `p2kb_obex_find` only because the index is title-keyed. Row S-249 and observation O26 should be reclassified (the residual `serial.MODE_NONE` defect is specced).
3. **NF-3 — `smart-pins/smart-pin-11001-adc-external-clock.yaml:77`, `:115`** `long    %0000_0000_000_100011_0000001_00_11001_0  ' P_PLUS1_B for clock`: the literal puts a `1` in M[0] (D[8]) and none in the B selector (BBBB = D[27:24]); `P_PLUS1_B` is `%0000_0001_000…` (v55:1426-1444 pattern; SD:3745-3755). Correct: `long    P_ADC_EXT | P_PLUS1_B  ' B input = the clock pin (pin+1)` — the constants form compiles (`a244_ext_mode_constants`) and matches the same file's Spin2 lines `:53`, `:130`. `:151` `required_pin_config: "%100011_00000000_00_11001_0"` (22 bits) → `"P_ADC_EXT | P_PLUS1_B"`. Whether the external-clock pin also needs M[12:10] = %100 is **not stated by SD:4262** (UNVERIFIED; the page's Spin2 lines omit it).
4. **NF-4 — `smart-pins/smart-pin-11010-adc-scope-trigger.yaml:53`, `:97`, `:131`**: the Spin2 `pinstart(adc_pin, P_ADC_SCOPE, …)` carries no ADC-enable bits while the same page's PASM literal (`:77`) and `required_pin_config` (`:131`, "`%100011` in bits 17:12" — the field is D[20:15]) say the pin needs M[12:10] = %100. Self-contradiction; the source (SD:4509-4546) does not say whether scope mode needs it → UNVERIFIED. Correct text if the page's PASM is right: `P_ADC_SCOPE | P_ADC_1X` at `:53`,`:97` (both blocks compile with `-d`, `a221_11010_b0_adc1x`, `a221_11010_b1_fix_adc1x`) and `:131` `required_pin_config: "P_ADC_1X (M[12:10] = %100); mode word %100011_0000000_00_11010_0"`. Decision D2.
5. **NF-5 — `language/spin2/methods/wxpin.yaml:91-102`** `mode_specific_x_values`: `:94` `P_PULSE: "High time period"` → `"X[15:0] base period, X[31:16] compare value (SD:3970-3972)"`; `:96` `P_NCO_FREQ: "Frequency value"` → `"X[15:0] base period, X[31:16] initial phase; the frequency step is Y (SD:4004-4010)"`; `:100` `P_QUADRATURE: "Filter period"` → `"Measurement period in clocks (0 = continuous totalizer) (SD:4095-4097)"`. (`:98-99` "Frame period" is the frame in base periods, X[31:16], SD:4040 — acceptable.)
6. **NF-6 — `system-registers/complete-system-registers-index.yaml:315-316`**: `register_access_speed: "All register access completes in single clock cycle"` (CSV: most instructions take 2 clocks) and `hub_access_timing: "PTRA/PTRB hub access follows hub timing rules (0-7 clock delay)"` (hub reads are 9...16 clocks, CSV:178) — unsourced (inferred).
7. **NF-7 — the `:label` local-label spelling** (`pasm-labels.yaml:29-35,38,59-61,68,90-92`; `identifier-rules.yaml:133,141-144`) has no ingested source (greps of SD, v55, v51 text, PASM2 manual, datasheet: none); pnut-ts accepts it as the dot form's twin. Add to the PNut check (a new punch-list item: does PNut accept `:label`?) — decision D6.
8. **NF-8 — `sources/spin2-v51/experimental-findings.md:9-12,73-80`** (pnut_ts v1.51.5, 2025-09-03): 31-35-character symbols compiled and were not truncated; pnut-ts v1.55.8 rejects ≥31 (`s251_*`). A lead for punch-list item 7 (the limit changed between PNut-TS releases, or the check is new).
9. **NF-9 — `external-inputs/source-code/obex-projects/2842-Full_Duplex_Serial/jm_fullduplexserial.spin2:403`** (`pub format(p_str, p_args) | idx, c, asc, field, digits`): `field` is a reserved word in v1.55.8 (`Expected a unique variable name … (m241)`); the unmodified object does not compile, so any KB page that tells readers to use it with the current compiler needs the note (the same class as `reference_doc_example_code_predates_keywords`). Ingested file — not edited.
10. **NF-10 — `language/spin2/patterns/applications/debug_enabled.yaml:82-83`** `string("Memory free: ", dec(memory_free))`: `string()` takes literals, and `dec()` is a method of a FullDuplexSerial-style object, not a built-in (and `:70` calls `debug_out.printf`) — a G5 page; same family as NF-1.
11. **NF-11 — `smart_pins.yaml:48`** `configuration: "Per-pin 16-bit configuration"` — the WRPIN D is 32 bits (`%AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0`, SD:3731); `:546-547` `max_toggle_rate: "Clock/2 (synchronous modes)"`, `async_serial: "Clock/16 (typical UART limit)"` have no source (SD:4640-4738 gives none).
12. **NF-12 — change-note wording in served YAML**: ≈10 served scalars and ≈14 YAML comments, listed under S-241 (class sweep). Decision D5.
13. **NF-13 — `hardware/addon-serial-host.yaml:96-106,132-161`** and the other add-on pages' `use_cases`/`applications`/`advantages` blocks: capability lists beyond the Product Guide (only the three files of S-258 were read).
14. **NF-14 — `architecture/p2-architecture-mental-model.yaml:130-137`** (`cordic`: "7-8 operations in flight", "55 clocks per operation", "1 result per COG every 8 clocks") — not re-read against SD:3413 and G7G8 NF-1 (CORDIC overlap); flagged, not specced.

## Decisions for the sprint / for Stephen

- **D1 (sprint) — smart-pin combined listings: which side to rename (S-220).** Recommend renaming the **PASM registers** (`*_reg`, `bit_clks`) and declaring them with `res`: 6 DAT edits against 6 PUB rewrites, and the Spin2 half is what readers copy. Alternative: rename the Spin2 locals.
- **D2 (Stephen/arbiter) — scope mode needs ADC bits? (NF-4, NF-3).** The source is silent on whether `%11010` and `%11001` need M[12:10] = %100. Options: (a) make the page self-consistent with its PASM literal (`P_ADC_SCOPE | P_ADC_1X`) — recommended, compiled; (b) a bench run (a free pin P0-P7/P32-P47, jumper to 3.3 V, read `RDPIN` in each form) — only if (a) is not acceptable. Sources are silent: search `M.[12..10]` over `silicon-doc-text.txt` hits only :3808-3813 (repository/DAC modes), :3923/:3934/:3951 (DAC modes) and :4262 (the **internally** clocked ADC) — the scope section :4509-4575 and the external-clock text :4262 (second sentence) do not mention it; v55:1466-1473 lists only the input-range constants. Control hit: the same search does find the internal-ADC statement. Jumper-testable on a free pin (P0-P7/P32-P47, pin tied to 3.3 V, compare `RDPIN` in both forms).
- **D3 (sprint) — S-226 `servo_pulse`.** Delete it (recommended: a 20 ms period cannot be a 16-bit base period and NCO duty is not a frame-based pulse). Alternative: replace by a sawtooth-PWM servo example (new content to author and verify; not specced).
- **D4 (sprint) — S-244 example.** Keep the 320-clock `WYPIN` override with the trim-only post-processing (recommended, source-faithful) or revert the example to the source's 128-clock form with `SHR x,#7` / `ZEROX x,#13` (SD:4474-4489).
- **D5 (Stephen) — change notes (S-241, NF-12).** Delete the one named line now (trivially safe); for the other served scalars and comments choose: delete all (recommended — the KB states what is true now), or leave the provenance-carrying `source:` locators and delete only the "previously …" sentences.
- **D6 (Stephen) — the `:label` local-label spelling (S-264, NF-7).** (a) Delete it from the teaching pages until PNut confirms (recommended; S-250's example already uses the dot form), (b) keep it with "accepted by pnut-ts; not in any Parallax document". Add the PNut question to the punch list either way.
- **D7 (sprint) — S-256.** Adopt the data change to `_code-keys.yaml` plus the `pasm2-getting-started.yaml:522-529` restructure (recommended), or add the generic keys `simple`/`multiple` (cheaper, noisier).
- **D8 (Stephen) — `tools/pnut-ts-compiler.yaml` (S-257).** (a) Fix the command name, delete `common_errors`, point to `--help` for the options (recommended: tool behaviour is not a KB fact); (b) retire the page. `pnut-term-ts` options stay NOT CHECKED either way.
- **D9 (Stephen) — "Silicon Doc" in served `source:` lines (S-265).** ≈90 files; the memory rule bans codenames in documents. Options: replace in the 10 named sites only (recommended now), or a mechanical tree-wide replacement to the official title in a later pass.
- **D10 (sprint) — S-251.** No edit to the length claim until PNut answers (punch list 7); apply the miscount fixes in whichever branch.
- **D11 (sprint) — S-225 `wxpin.yaml` siblings (NF-5)** ride with the S-225 pass.

## Tally

Rows: 61. Change spec 44 (code compiled in 28: S-220..S-233, S-236, S-239, S-242..S-245, S-250, S-252..S-255, S-260, S-263, S-264 — plus the S-249 residual; prose / YAML-level "compile in sprint" in 16: S-234, S-235, S-237, S-238, S-240, S-241, S-246, S-248, S-256, S-257, S-258, S-259, S-262, S-265, S-266, S-278 — and the prose lines inside S-225, S-233, S-236). Pointers 14 (S-247, S-261, S-267..S-277, S-279). Reclassified 1 (S-249). Undetermined 2 (S-251, S-280). Bench questions 0. New findings 14. Decisions 11.
