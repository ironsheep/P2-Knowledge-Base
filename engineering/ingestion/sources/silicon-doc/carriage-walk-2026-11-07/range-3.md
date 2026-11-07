# Silicon Doc carriage walk, range 3: SD:1198-2034

Pixel operations, DACs, streamer (with DDS/Goertzel and DVI), colorspace converter, I/O pin timing,
cog attention. KB = `deliverables/ai/P2/`; `pasm2/` = `language/pasm2/`; `strm/` = `architecture/streamer/`.

## Sections

| SD line | Heading | Disposition |
|---|---|---|
| 1198 | PIXEL OPERATIONS | Encodings, 7 clocks and one-line semantics carried; formula and Table 13 not carried, already IN-PLAN §7 |
| 1258 | DACs | Pin mapping carried (`strm/dac-routing.yaml`); "SETDACS is the background, streamer/colorspace override it" only implied |
| 1275 | STREAMER (intro, NCO, commands, mode table, %dddd, %e/%w, %ppp, %a) | Well carried across `strm/*.yaml` and `x*.yaml`. Gaps: per-mode lane layout column, stop-releases-overrides. One concept page states wrong mode codes and a wrong XINIT/XCONT operand meaning (MISMATCH) |
| 1462 | Immediate -> LUT -> Pins/DACs | LUT base carried; "last value repeats" not carried |
| 1466 | Immediate -> Pins/DACs | "Last value repeats" not carried |
| 1470 | RDFAST -> LUT -> Pins/DACs | S[3:0] base carried; refill on last value not stated |
| 1474 | RDFAST -> Pins/DACs | Mode list carried; shift/refill rule not stated |
| 1478 | RDFAST -> RGB -> Pins/DACs (Tables 14-18) | Mode names carried; LUMA8 S[2:0] colour, RGBI8 table, bit expansions and X3/X2/X1/X0 = R/G/B/0 not carried |
| 1533 | Pins -> DACs/WRFAST | Fully carried (`strm/pin-selection.yaml`) |
| 1537 | ADCs/Pins -> DACs/WRFAST | Mode names only; SETSCP prerequisite, S[1:0]/S[1] channel select and word layout not carried |
| 1553 | DDS/Goertzel (incl. Table 19 program, SINC2 note) | Well carried (`strm/dds-goertzel.yaml`, `pasm2/getxacc.yaml`); SINC2 accumulation formula only named |
| 1707 | Digital Video Output (DVI/HDMI), Tables 20-22 | Not carried: CMOD[8:7], pin order, TMDS/literal select, 10x clock rule. `nco-timing.yaml` gives HDMI 720p NCO values that the 10x rule rules out (MISMATCH) |
| 1849 | COLORSPACE CONVERTER (Table 23) | Not carried beyond parameter names and widths on five `setc*` pages |
| 1961 | I/O PIN TIMING | Fully carried (`architecture/io_pin_timing.yaml`, `drvl/drvh/testp/testpn`); findability IN-PLAN §8 |
| 2013 | COG ATTENTION | Carried (`architecture/cog_attention.yaml`, `pasm2/cogatn.yaml` and the four monitor pages) |

## Ledger

| SD lines | Fact | C/M | YAML home | Disposition | Note |
|---|---|---|---|---|---|
| 1200 | Pixel ops take 7 clocks | C | `pasm2/addpix.yaml:18-25`, `mulpix/blnpix/mixpix.yaml:8-11` | MATCH | `cycles: 7` |
| 1202-1205 | ADDPIX saturating add, MULPIX $FF=1.0, BLNPIX by SETPIV, MIXPIX by SETPIX/SETPIV | C | `addpix.yaml:5`, `mulpix.yaml:12`, `blnpix.yaml:12`, `mixpix.yaml:12` | MATCH | e.g. "where $FF = 1.0 and $00 = 0.0" |
| 1210-1211 | SETPIV V[7:0]=D[7:0]; SETPIX M[5:0]=D[5:0] | C | `setpiv.yaml:12`, `setpix.yaml:12` | MATCH | "Set MIXPIX mode to D[5:0]" |
| 1214-1255 | Sum-of-products formula and DMIX/SMIX Table 13 | C | NOT-CARRIED | IN-PLAN §7 | grep `DMIX\|SMIX\|sum-of-products`: 0 hits |
| 1260-1265 | DACn drives pins %XXXXnn | C | `strm/dac-routing.yaml:158-165` | MATCH | "DAC0: Pins %xxxx00 ..." |
| 1270 | SETDACS byte 3..0 -> DAC3..0 | C | `pasm2/setdacs.yaml:12` | MATCH | page `category: Smart Pin` (a misfile, minor) |
| 1272 | SETDACS values output constantly except while streamer/colorspace override | C | `strm/dac-routing.yaml:29,153` | PARTIAL | "No override (SETDACS value used)"; not on `setdacs.yaml`; colorspace override not mentioned |
| 1277 | Streamer outputs to pins/DACs, captures pins/ADC, Goertzel | C | `strm/overview.yaml:29-35` | MATCH | |
| 1281-1285 | Five streamer instructions and their meaning | C | `strm/overview.yaml:81-110`; `xinit/xzero/xcont/setxfrq/getxacc.yaml` | MATCH | |
| 1285 | GETXACC reads the Goertzel X/Y accumulators | C | `pasm2/setxfrq.yaml:81` | MISMATCH | YAML: "GETXACC: Read phase accumulator (Goertzel mode)". `getxacc.yaml:12` is right |
| 1288-1292 | NCO `phase = (phase & $7FFF_FFFF) + frequency`; MSB = rollover; DDS runs every clock | C | `strm/nco-timing.yaml:17-30`; `dds-goertzel.yaml:84-87` | MATCH | |
| 1294-1305 | SETXFRQ multiplier $8000_0000, table, +1 on remainder | C | `strm/nco-timing.yaml:33-90`; `setxfrq.yaml:50-77` | MATCH | 1/3 `$2AAA_AAAB`, 1/5 `$1999_999A`; 1/6, 1/7 absent (rule covers them) |
| 1296 | $8000_0000 is the value on cog start | C | `setxfrq.yaml:77` | MATCH | "stated by the source as the default value on cog start" |
| 1307 | SETQ before XINIT/XZERO/XCONT sets the frequency on the command's first clock; without SETQ it is unchanged | C | `setxfrq.yaml:44-49`; `nco-timing.yaml:137-143` | MATCH | |
| 1309 | D = mode+duration, S = data, sub-mode or ignored | C | `xinit.yaml:101` | MATCH | but see the next row |
| 1309, 1313 | XINIT/XCONT S is data, count is D[15:0] | C | `pasm2/concepts/streamer_smartpin_control.yaml:26-30,44` | MISMATCH | YAML: `syntax: "XINIT mode, count"`, `count: "Transfer count"`, `syntax: "XCONT mode, count"` |
| 1311 | One-level command buffer: two commands accepted before waiting; XINIT-then-XCONT lets a smart pin be set up in between | C | `strm/overview.yaml:40`; `xcont.yaml:62` | PARTIAL | "Single-level (one pending command)"; the XINIT+XCONT smart-pin coordination idiom is not stated |
| 1313-1397 | Mode table D[31:16] templates | C | `strm/modes-reference.yaml:97-388`; `language/spin2/symbols/streamer-symbols.yaml` | MATCH | spot-checked all rows: mode nibble and d_19_16 agree |
| 1313-1397 | Mode table codes | C | `pasm2/concepts/streamer_smartpin_control.yaml:54-71` | MISMATCH | YAML: immediate 1-bit `%0000_0000` ... 32-bit `%0000_0101`; LUT `%0001_0000`..`%0001_0011`; RFBYTE `%0010_xxxx`. SD: immediate->pins is `%0100`-`%0111`, `%0000`-`%0011` are the LUT modes, RDFAST->pins is `%1000`-`%1011` |
| 1316-1391 | Per-mode lane layout column ($X3_X2_X1_X0: which bits land in which DAC channel) | C | NOT-CARRIED | NOT-CARRIED | grep `aaaaaaaa\|babababa\|dcba\|X3_X2`: 0 hits in `strm/`; modes-reference gives only "N DAC ch x M bits" |
| 1387-1391 | ADC modes have no pin field (`w---`) | C | `strm/overview.yaml:134-135`; `modes-reference.yaml:49-51` | PARTIAL | YAML says "D[22:20] are fixed zeros"; SD marks them `---` (unused). Same practical effect, not exact |
| 1401 | D[15:0] decrements each rollover; at count 1 a buffered XZERO/XCONT begins seamlessly; else goes to 0 | C | `strm/overview.yaml:112-118`; `xinit.yaml:103` | MATCH | |
| 1401 | At count 0, or set to 0, the streamer stops and all streamer DAC overrides and pin outputs cease | C | `xinit.yaml:105` ("A count of 0 stops the streamer") | PARTIAL | that the DAC overrides and pin outputs are released (DACs revert to SETDACS, pins to OUT) is not stated; grep `cease\|overrides\? cease\|revert`: 0 |
| 1403 | $FFFF runs perpetually | C | `strm/overview.yaml:115-122`; `xinit.yaml:102` | MATCH | |
| 1405 | XINIT restarts from any state; `XINIT #0,#0` stops; XSTOP is its alias | C | `strm/overview.yaml:102-105`; `xzero.yaml:49`; `xcont.yaml:61` | MATCH | |
| 1407 | XZERO/XCONT wait for the prior command's last clock; none if count is 0; next rollover if $FFFF | C | `xcont.yaml:60` | PARTIAL | carried on XCONT only; `xzero.yaml` says nothing about waiting or the $FFFF case |
| 1409 | XZERO zeroes phase; with ~1/3 fractions a 1-clock glitch every ~30 s unless XZERO is used at hsync; +1 so rollover lands on clock N | C | `xzero.yaml:12-15`; `nco-timing.yaml:145-153` | PARTIAL | "prevents drift accumulation"; the 1-clock glitch is not stated |
| 1411 | XCONT keeps phase | C | `xcont.yaml:12,58` | MATCH | |
| 1414 | Pin must be in DAC mode with COGID, DIR high | C | `strm/dac-routing.yaml:167-171` | MATCH | adds TT=%01 from EF |
| 1416-1436 | %dddd D[27:24] override table | C | `strm/dac-routing.yaml:22-149` | MATCH | 16 rows compared |
| 1439 | Output modes OR the streamer output with {OUTB,OUTA}; %e must be 1 | C | `strm/pin-selection.yaml:126-143` | MATCH | |
| 1441 | Input modes read {INB,INA}; %w enables WF* | C | `strm/pin-selection.yaml:145-165` | MATCH | |
| 1443-1452 | %ppp D[22:20] pin groups with wrap | C | `strm/pin-selection.yaml:30-65` | MATCH | 8 rows compared |
| 1454 | Sub-8-pin modes use D[19..17] | C | `strm/pin-selection.yaml:68-95` | MATCH | |
| 1456 | Bottom-first default; %a D[16] makes it top-first within bytes | C | `strm/pin-selection.yaml:185-208` | MATCH | |
| 1458-1460 | RDFAST/WRFAST must be done beforehand | C | `strm/overview.yaml:49,65`; `pin-selection.yaml:168-171` | MATCH | |
| 1464 | Imm->LUT: S shifted by 1/2/4/8 per rollover, **last value repeating**; LUT base `%bbbb00000` from D[19:16] | C | `strm/modes-reference.yaml:103` | PARTIAL | base carried; shift-and-last-value-repeats not carried (grep `repeat\|last value`: 0 in `strm/`, `x*.yaml`) |
| 1468 | Imm->Pins: values shifted per rollover, last value repeating | C | NOT-CARRIED | NOT-CARRIED | same searches |
| 1472 | RDFAST->LUT: RFLONG refilled after last value; base in S[3:0] | C | `strm/modes-reference.yaml:186` | PARTIAL | S[3:0] carried; refill rule not |
| 1476 | RDFAST->Pins: RFBYTE/WORD/LONG refilled after last value | C | `strm/overview.yaml:47-50` | PARTIAL | the mode list only |
| 1480 | RGB modes output {R,G,B,0} to X3,X2,X1,X0 | C | NOT-CARRIED | NOT-CARRIED | grep `X3.{0,20}red\|X0.{0,10}\$00\|8'b0`: 0 hits |
| 1482-1494 | LUMA8: S[2:0] selects colour (Table 14) | C | `strm/modes-reference.yaml:265-268` | NOT-CARRIED | only "RFBYTE -> 8-bit luminance -> RGB"; grep `S\[2:0\]\|orange\|magenta` in `strm/`, `pasm2/`: 0 |
| 1497-1509 | RGBI8 colour table and 5-bit expansion (Table 15) | C | `strm/modes-reference.yaml:272` | PARTIAL | "upper 3 bits select a colour, lower 5 bits are intensity"; the colour assignments and expansion are absent |
| 1512-1531 | RGB8/RGB16/RGB24 bit expansions (Tables 16-18) | C | NOT-CARRIED | NOT-CARRIED | grep `P\[15:11\]\|replicat`: 0; only "3:3:2", "5:6:5", "8:8:8" |
| 1535 | Pins->WRFAST reads {INB,INA}; 1/2/4-pin modes WFBYTE every 8 bits | C | `strm/pin-selection.yaml:153-165` | MATCH | quotes the line |
| 1541 | ADC capture needs SETSCP first; the pins in ADC sample or ADC scope smart-pin mode, enabled | C | NOT-CARRIED | NOT-CARRIED | grep `SETSCP` in `strm/`: 0. `smart-pin-11010-adc-scope-trigger.yaml:142` mentions SETSCP feeding the streamer, but not the prerequisite or the mode requirement |
| 1543-1545 | 1-ADC8: S[1:0] picks the channel; 2-ADC8: S[1] picks upper/lower pair | C | `strm/overview.yaml:135` ("the channel is chosen in S[1:0]") | PARTIAL | S[1] for 2-ADC8 not carried; grep `S\[1\]`: 0 |
| 1549 | ADC+pin modes: pins in the low half, SCOPE channels in the high half | C | NOT-CARRIED | NOT-CARRIED | grep `upper half\|lower half` in `strm/`: 0 |
| 1555-1557 | DDS: every clock, LUT long -> X3..X0 with MSB inverted; bytes 3,2 feed Goertzel | C | `strm/dds-goertzel.yaml:84-112` | MATCH | "LUT.byte[3] ^ $80" |
| 1559 | GETXACC results -> QVECTOR for power/phase | C | `dds-goertzel.yaml:197-201`; `getxacc.yaml:20` | MATCH | |
| 1563 | %pppp D[22:19] block, base = %pppp*4; raw ADC, no smart mode; 0=-1/1=+1; 2/4-channel sum shifted right 1 | C | `dds-goertzel.yaml:36-52,79` | MATCH | |
| 1565-1583 | S[19:16] invert, S[15:12] sum | C | `dds-goertzel.yaml:53-55` | MATCH | |
| 1586-1600 | S[11:0] loop-size table and %A/%T rule | C | `dds-goertzel.yaml:56-69,121-137` | MATCH | 8 rows compared |
| 1602 | sin byte 3, cos byte 2 multiplied by sum -3..+3, into 32-bit accumulators | C | `dds-goertzel.yaml:106-112,140-142` | PARTIAL | 32-bit accumulator width not stated |
| 1604 | GETXACC: cos -> D, sin -> next S; capture and clear; repeat reads equal until a new command | C | `getxacc.yaml:12-34`; `dds-goertzel.yaml:166-191` | MATCH | carries the documented behaviour plus Rev C errata E4/E5 (EF-069, EF-070) |
| 1606-1618 | D[23] SINC1/SINC2; SINC2 formula `SIN_MUL += ...; SIN_ACC += SIN_MUL` | C | `dds-goertzel.yaml:20-33,106-112`; `getxacc.yaml:84` | PARTIAL | D[23] select carried; the calculation block shows SINC1 only, SINC2 is just "double integration" (grep `SIN_MUL`: 0) |
| 1621-1694 | Goertzel demo program | C | `dds-goertzel.yaml:146-164,264-297` | MATCH | table builder and `dds_d`/`dds_s` longs reproduced |
| 1702 | SINC2 needs reduced amplitude (+/-10 versus +/-127) | C | `dds-goertzel.yaml:26-33,236-239` | MATCH | |
| 1704-1705 | SINC2 corrupts readings when the iteration count varies; use power-of-two clocks per cycle | C | `getxacc.yaml:84` | MATCH | quotes "off by a single clock cycle" |
| 1709 | DVI: streamer's 32-bit output becomes 8 pins of RED/GRN/BLU/CLK pairs | C | NOT-CARRIED | NOT-CARRIED | grep `DVI\|TMDS\|CMOD\[` in `architecture/`, `language/`: only `nco-timing.yaml:127` "Requires 10x for TMDS" |
| 1711-1718 | SETCMOD bits 8:7 select DVI; Table 20 pin order fwd/rev | C | `pasm2/setcmod.yaml:12` | NOT-CARRIED | page says only "CMOD parameter to D[8:0]" |
| 1721-1748 | P[1]=0 TMDS-encode 8-bit RGB; P[1]=1 send 10-bit literal (syncs) | C | NOT-CARRIED | NOT-CARRIED | same searches |
| 1751 | DVI needs sysclk = 10x pixel rate (250 MHz for 640x480) | C | `strm/nco-timing.yaml:122-127` | MISMATCH | YAML gives `hdmi_720p` NCO values for a 74.25 MHz pixel rate at 250/300/320 MHz clocks (`$2604_1894` ...). In DVI mode the NCO must be 1/10 of the clock, so none of those values can drive HDMI |
| 1753 | NCO $0CCCCCCC+1 for DVI | C | `nco-timing.yaml:82-85` | MATCH | "$0CCC_CCCD ... (HDMI 10x)" |
| 1755-1845 | 640x480 HDMI demo (mode longs `$70810000`, `$B0850000`, sync longs) | C | NOT-CARRIED | NOT-CARRIED | grep `setcmod #\$100\|B0850000\|70810000`: 0 |
| 1851 | Colorspace converter per cog: matrix plus modulation of DAC channels | C | `pasm2/setcy.yaml:12` etc. | PARTIAL | names only |
| 1855-1859 | SETCY/CI/CQ/CFRQ D[31:0], SETCMOD D[8:0] | C | `setcy/setci/setcq/setcfrq/setcmod.yaml:12` | MATCH | |
| 1861 | DAC3/2/1 = R/G/B; 5-clock group delay in use | C | NOT-CARRIED | NOT-CARRIED | grep `group delay\|five clocks`: 0 |
| 1863-1867 | CMOD[4] sign/zero extend; Y/I/Q matrix /128; 128 = unity | C | NOT-CARRIED | NOT-CARRIED | grep `CMOD\[`: 0 |
| 1869-1874 | PHS -= CFRQ; 5-stage CORDIC, IQ x 1.646; CFRQ = $1_0000_0000 * f / clk | C | NOT-CARRIED | NOT-CARRIED | grep `1\.646`: 0 |
| 1876-1890 | FY/FI/FQ/FS/FIQ/FYS/FYC terms, CMOD[3:0] | C | NOT-CARRIED | NOT-CARRIED | |
| 1893-1958 | CMOD[6:5] output select (Table 23) | C | NOT-CARRIED | NOT-CARRIED | `strm/overview.yaml:68-71` says only that the converter is a separate stage |
| 1965-1973 | DIRx/OUTx/INx; OUT needs DIR high | C | `architecture/system-registers/complete-system-registers-index.yaml:137-154` | MATCH | "1=output enabled, 0=input/high-Z"; own-DIR gating question is IN-PLAN §9 arm J |
| 1977-1980 | DIR*/OUT*/FLT*/DRV* families: FLT clears DIR, DRV sets DIR | C | `pasm2/fltl.yaml:4-8`, `drvl.yaml:13-14` | MATCH | |
| 1984-1985 | TESTP/TESTPN with WC/WZ/AND/OR/XOR | C | `testp.yaml:3-23`, `testpn.yaml:26-46` | MATCH | |
| 1987-1994 | DIR/OUT change: 3 more clocks before the pin moves | C | `architecture/io_pin_timing.yaml:42-59`; `drvl.yaml:7-11`, `drvh.yaml:12-15` | MATCH | quoted; findability IN-PLAN §8 |
| 1997-2003 | INx read = pins 3 clocks before the instruction | C | `io_pin_timing.yaml:61-73` | MATCH | |
| 2005-2011 | TESTP/TESTPN = 2 clocks before | C | `io_pin_timing.yaml:75-87`; `testp.yaml:27-29`; `testpn.yaml:23-25` | MATCH | |
| 2017 | COGATN takes 2 clocks | C | `cogatn.yaml:27-35` | MATCH | |
| 2020 | D bits 0..15 = cogs 0..15; strobes ORed into one composite set | C | `cogatn.yaml:5-8`; `cog_attention.yaml:70-76` | MATCH | `cog_attention.yaml:22` "8x8" signal matrix is narrower, but it frames the 8-cog part (`:24-26`) |
| 2024-2030 | POLLATN/WAITATN/JATN/JNATN | C | `cog_attention.yaml:83-131` | MATCH | |
| 2033 | Several requesters need a hub-RAM message structure; the intended case is a known sender | C | `cogatn.yaml:11-14` | MATCH | |

Mechanism rows: none of substance in this range. The colorspace pipeline formulas (SD:1865-1890) are on
the line: a composite or VGA driver writer programs CY/CI/CQ/CMOD from them, so they are counted as contract.

Counts: MATCH 47, PARTIAL 14, MISMATCH 4, NOT-CARRIED 16, IN-PLAN 1.

## Findings

### MISMATCH

1. **`pasm2/concepts/streamer_smartpin_control.yaml:54-71`: wrong streamer mode codes.**
   YAML: `immediate_modes: 1_bit_output: "%0000_0000" ... 32_bit_output: "%0000_0101"`,
   `lut_modes: 1_bit_lut: "%0001_0000" ...`, `rfbyte_modes: rfbyte_fetch: "%0010_xxxx"`.
   SD:1320-1360: `0000`-`0011` are "imm -> 32/16/8/4 x N-bit LUT"; "Immediate -> Pins/DACs" is
   `0100`-`0111`; "RDFAST -> Pins/DACs" is `1000`-`1011`. An agent composing a command word from this
   page gets LUT modes when it asked for direct output, and an immediate mode when it asked for RFBYTE.
   The correct table is in `strm/modes-reference.yaml`. Searches: read the page; compared it with SD
   1313-1397.
2. **`pasm2/concepts/streamer_smartpin_control.yaml:26-30,44`: the XINIT/XCONT S operand is called a count.**
   YAML: `syntax: "XINIT mode, count"`, `count: "Transfer count"`; `syntax: "XCONT mode, count"`.
   SD:1309 "S/# supplies various data, or is ignored"; SD:1313 "D/#[15:0] conveys the number of NCO
   rollovers". Code written from this page puts the count in S. `xinit.yaml:101` states it correctly.
3. **`strm/nco-timing.yaml:122-127`: HDMI 720p NCO values contradict the DVI 10x rule.**
   YAML: `hdmi_720p: pixel_rate: "74.250 MHz" at_250mhz: "$2604_1894" ... note: "Requires 10x for TMDS"`.
   SD:1751 "Digital video output mode requires that the P2 clock frequency be 10x the pixel rate";
   SD:1753 "The NCO frequency must be set to 1/10 of the main clock using the value $0CCCCCCC+1". In DVI
   mode the NCO is always 1/10 of the clock, and 720p would need a 742.5 MHz clock. The values
   are arithmetically right for some streamer mode, but under an `hdmi_720p` key they are wrong.
4. **`pasm2/setxfrq.yaml:81`: GETXACC described as reading the phase accumulator.**
   YAML: `GETXACC: Read phase accumulator (Goertzel mode)`. SD:1285 "Get Goertzel X into D and Y into
   next S"; SD:1604 it captures the sine and cosine accumulations. The NCO phase is not readable.
   `getxacc.yaml:12` is correct; the cross-reference on the SETXFRQ page is wrong.

### NOT-CARRIED (contract)

5. **Colorspace converter (SD:1851-1958).** The KB states only that SETCY/CI/CQ/CFRQ take D[31:0] and
   SETCMOD takes D[8:0]. Not carried: the CMOD bit map (CMOD[8:7] DVI, [6:5] output mode, [4] sign
   extension, [3:1] DAC0 add-in, [0] sync polarity); the Y/I/Q matrix with /128 and 128 = unity; the
   modulator `PHS -= CFRQ`, the 1.646 gain and `CFRQ = $1_0000_0000 * f / clk`; the FY..FYC terms; the
   Table 23 output modes; the 5-clock group delay. No VGA, component or composite driver can be
   written from the KB. Searches: `colorspace`, `CMOD\[`, `1\.646`, `group delay`, `composite`, `NTSC`,
   `S-Video` across `architecture/`, `language/`. Agents would look at `pasm2/setcmod.yaml` (or a
   `strm/` colorspace page, which does not exist).
6. **DVI/HDMI output (SD:1709-1753).** SETCMOD %10/%11 in bits 8:7 select DVI forward or reverse;
   Table 20 pin order (`RED+ RED- GRN+ GRN- BLU+ BLU- CLK+ CLK-` and the reverse); P[1]=0 TMDS-encodes
   the RGB bytes and P[1]=1 sends 10-bit literals (syncs); sysclk = 10x the pixel rate. Searches: `DVI`,
   `TMDS`, `CMOD`, `setcmod #\$100`, `70810000`, `B0850000`. Agents would look at `setcmod.yaml`,
   `strm/modes-reference.yaml`, `hardware/addon-digital-video-out.yaml` (which says only that the
   streamer drives TMDS).
7. **ADC capture modes (SD:1539-1551).** SETSCP must be set first; the pins must be in an ADC sample
   or ADC scope smart-pin mode and enabled; S[1:0] selects one channel and S[1] selects the upper or lower pair;
   pin data goes in the low half of the word and SCOPE data in the high half. Only S[1:0] appears
   (`strm/overview.yaml:135`). Searches: `SETSCP`, `S\[1\]`, `upper half`, `lower half`, `scope
   channel` in `strm/`. Agents would look at `strm/modes-reference.yaml` adc_modes or `pin-capture.yaml`.
8. **Immediate modes: the last value repeats (SD:1464, :1468).** Once the S data is used up, the last
   1/2/4/8/16-bit value repeats on every further rollover. A count larger than 32/width keeps
   outputting the top value; this is a common idle-level idiom (e.g. a long count of a 1-bit pattern). Searches:
   `repeat`, `last value`, `shifted by` in `strm/` and `x*.yaml`. Agents would look at
   `strm/modes-reference.yaml` or `xinit.yaml`. The RDFAST refill-on-last-value rule (SD:1472, :1476) is
   the same gap.
9. **RGB mode output (SD:1480-1531).** {R,G,B,0} goes to X3/X2/X1/X0; LUMA8 takes its colour from
   S[2:0] (Table 14: %000 orange ... %111 white); the RGBI8 colour assignment; the RGB8/16/24 bit
   replication. Without it an agent cannot set LUMA8's S operand or route RGB to the right DAC pins.
   Searches: `S\[2:0\]`, `orange`, `magenta`, `P\[15:11\]`, `replicat`, `X3.{0,20}red`. Look-up page:
   `strm/modes-reference.yaml` rgb modes.
10. **Per-mode DAC lane layout (SD:1316-1391, the `$X3_X2_X1_X0` column).** Which data bits reach which
    DAC channel in each mode (e.g. `0110 ... p10a`: `%..._dcbadcba`, one 4-bit value replicated in X0;
    `p01a`: two 2-bit values X1/X0). `modes-reference.yaml` gives only "N DAC ch x M bits". Searches:
    `aaaaaaaa`, `babababa`, `dcba`, `X3_X2`. This interacts with `dac-routing.yaml`'s %dddd table,
    which assumes the reader knows what X0..X3 hold.

Lesser gaps (PARTIAL, listed in the ledger): the streamer releasing DAC overrides and pin outputs at count 0
(SD:1401); XZERO's wait semantics missing from `xzero.yaml` (SD:1407); the XZERO 1-clock glitch
(SD:1409); the SINC2 accumulation formula (SD:1615-1618); the 32-bit accumulator width (SD:1602);
`setdacs.yaml` not saying that the streamer and colorspace converter override it (SD:1272); and
`setdacs.yaml` filed under `category: Smart Pin`.
