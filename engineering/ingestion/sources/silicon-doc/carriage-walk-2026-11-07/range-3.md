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

## Closure (task «#455», 2026-11-09)

Each row was re-found by content, confirmed at its SD line, and checked against the YAML text as it
stands now. Fix lines are in the files as edited by this task. KB paths are relative to
`deliverables/ai/P2/`; `strm/` = `architecture/streamer/`; `pasm2/` = `language/pasm2/`. Ledger rows
are named by their SD lines and by their line in this file.

### Canonical home for the colorspace converter and DVI facts

- **Where agents look.** The local index (`deliverables/ai/p2kb-index.json`) sends `SETCMOD` and
  `setcmod` to `pasm2/setcmod.yaml`, `colorspace` to the `pasm2_colorspace` category (the five
  `setc*` files), and `DVI` / `HDMI` only to the add-on board's aliases
  (`hardware/addon-digital-video-out.yaml`). `TMDS`, `NTSC`, `composite` and `VGA` reach no
  converter or DVI content at all. The YAML text search found the facts in no file.
- **Choice: one new YAML file, `strm/colorspace-and-dvi.yaml`**, not blocks in existing files.
  - The CMOD register is shared: bits 8:7 select the streamer's DVI serialization (SD:1711) and
    bits 6:0 configure the converter (SD:1863-1893). Splitting them across `setcmod.yaml` and a
    streamer page would put half of one register's map in each.
  - The facts are tables (Table 20, Table 21, Table 23) and formula blocks. A single-instruction
    file may hold only its own instruction's facts, and five `setc*` files share them, so no one
    of them can be the home.
  - `strm/modes-reference.yaml` is the mode table; the converter is not a streamer mode, and the
    file is already the home of Tables 14-18.
  - The DVI rule (clock 10x the pixel rate, NCO `$0CCCCCCC+1`, SD:1751-1753) is stated once, at
    `strm/colorspace-and-dvi.yaml:198-204`; `strm/nco-timing.yaml:110` (see_also) links to it.
- **Links to the home:** `pasm2/setcmod.yaml:13` (cmod_fields) and `related:`;
  `pasm2/setcy.yaml`, `setci.yaml`, `setcq.yaml`, `setcfrq.yaml` `:13` (parameter_use) and
  `related:`; `pasm2/setdacs.yaml:20`; `strm/overview.yaml:36,76,216`; `strm/modes-reference.yaml:647`;
  `strm/nco-timing.yaml:110`; `strm/pin-selection.yaml:245-249`; `strm/_index.yaml:74-84`;
  `hardware/addon-digital-video-out.yaml:15-21,61`. Aliases are left to task «#463».
- **No table in two files.** The CMOD map, Tables 20, 21 and 23 and the converter formulas exist
  only in the new file. Tables 14-18 and the lane column exist only in `strm/modes-reference.yaml`.
  The 1 to 1/8 multiplier table exists only in `strm/nco-timing.yaml` (`setxfrq.yaml:40` points to
  it). The DAC pin mapping stays in `strm/dac-routing.yaml` (`setdacs.yaml` points to it).

### MISMATCH rows

| Ledger row | SD lines confirmed | Disposition | Fix (file:line) |
|---|---|---|---|
| 1285 GETXACC on the SETXFRQ page (line 39) | 1285, 1604 | CLOSED, fixed | `pasm2/setxfrq.yaml`: the GETXACC entry is removed from related_instructions (it is another instruction's content); the `related:` path `language/pasm2/getxacc.yaml` remains and carries the SD:1285 / instruction listing row 265 wording. |
| 1309, 1313 XINIT/XCONT operands (line 45) | 1309, 1313 | CLOSED, fixed | `pasm2/concepts/streamer_smartpin_control.yaml:26-32` (XINIT `{#}D,{#}S`; D = command in D[31:16] and NCO-rollover count in D[15:0]; S = data, sub-mode or ignored), `:43-47` (XCONT), `:49-54` (XZERO, same operands). |
| 1313-1397 wrong mode codes (line 48) | 1313-1397 | CLOSED, fixed | `streamer_smartpin_control.yaml:57-64`: the three wrong lists replaced by a one-sentence group summary and `mode_table: architecture/streamer/modes-reference.yaml`, the one home of the table. Searched the KB for `32_bit_output`, `rfbyte_fetch`, `%0001_0000` and `%0010_xxxx` as streamer codes: none remain. |
| 1751 `hdmi_720p` NCO values (line 92) | 1751, 1753 | CLOSED, fixed | `strm/nco-timing.yaml:77-80`: `hdmi_720p` removed, and with it the whole derived video_rates table (VGA 640x480 at 25.175 MHz, 800x600, 1024x768: no source states those values), now "Not documented"; the DVI rule at `strm/colorspace-and-dvi.yaml:198-204` is linked from `nco-timing.yaml:110` (see_also). The `(HDMI 10x)` note on the 1:10 row went with the derived 1:10 and 1:16 rows; the table at `:49-75` is the SD table (1, 1/2 ... 1/8, with 1/6 and 1/7 added). `grep hdmi_720p` and `74.25` over the KB: none. |

### NOT CARRIED rows

| Ledger row | SD lines confirmed | Disposition | Fix (file:line) |
|---|---|---|---|
| 1316-1391 per-mode lane layout (line 49) | 1316-1391 | CLOSED, fixed | `strm/modes-reference.yaml:140-600`: every one of the 56 rows carries `s_operand`, `pins` and `dac_lanes` copied from the S/#, Pins and DAC Channels columns; notation at `:128-135`. |
| 1468 immediate-to-pins, last value repeats (line 67) | 1464, 1468 | CLOSED, fixed | `strm/modes-reference.yaml:69-75` (immediate_direct.data); the LUT form at `:58-67`. |
| 1480 RGB modes {R,G,B,0} to X3..X0 (line 70) | 1480 | CLOSED, fixed | `strm/modes-reference.yaml:611-615` (rgb_modes.output); the five RGB rows' dac_lanes at `:400-438`; `strm/overview.yaml:76`. |
| 1482-1494 LUMA8 colour from S[2:0], Table 14 (line 71) | 1482-1494 | CLOSED, fixed | `strm/modes-reference.yaml:616-626`, 8 rows; the LUMA8 row's S operand at `:404`. |
| 1512-1531 RGB8, RGB16, RGB24, Tables 16-18 (line 73) | 1512-1531 | CLOSED, fixed | `strm/modes-reference.yaml:638-648`. |
| 1541 ADC capture needs SETSCP and an ADC sample/scope smart pin (line 75) | 1541, 3834-3836, 4555-4557 | CLOSED, fixed | `strm/modes-reference.yaml:653-657` (adc_modes.prerequisite), links to `pasm2/setscp.yaml` and the `11000`, `11001`, `11010` smart pin files at `:676-680`. |
| 1549 ADC plus pins: pins low half, SCOPE high half (line 77) | 1549 | CLOSED, fixed | `strm/modes-reference.yaml:662-665` (adc_modes.word_layout). |
| 1709 DVI output (line 89) | 1709 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:141-147`. |
| 1711-1718 SETCMOD bits 8:7 and Table 20 (line 90) | 1711-1718 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:148-182` (3 rows x 11 cells); `pasm2/setcmod.yaml:13` points to it. |
| 1721-1748 P[1] TMDS or literal, Table 21 (line 91) | 1721-1748 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:183-197`. |
| 1755-1845 640x480 DVI example (line 94) | 1755-1845 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:205-294`, the Table 22 program line for line (column layout only changed; the `file "birds_16bpp.bmp"` line kept, its file named in notes). It assembles: manifest entry `dvi.example.code`, fragment, wrap spin2-top, assumes `file:birds_16bpp.bmp`. The XZERO hsync subroutine is excerpted at `pasm2/xzero.yaml:31-38` and the visible-line loop at `pasm2/xcont.yaml:31-38`; the 32-pin mode words at a multiple-of-8 base at `strm/pin-selection.yaml:245-249`. |
| 1861 DAC3/2/1 = R/G/B, group delay 5 clocks (line 97) | 1861 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:56-64`. |
| 1863-1867 CMOD[4] and the /128 matrix (line 98) | 1863-1867; Datasheet p.2 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:65-78`. |
| 1869-1874 modulator, 1.646, CFRQ formula (line 99) | 1869-1874 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:79-91`, including SD's own $0B74_5CFE example; `pasm2/setcfrq.yaml:13` points to it. |
| 1876-1890 FY..FYC terms and CMOD[3:0] (line 100) | 1876-1890 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:92-110`. |
| 1893-1958 CMOD[6:5] output select, Table 23 (line 101) | 1893-1958 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:111-138` (4 rows x 6 cells). |

The walk's CMOD map was confirmed bit by bit at its SD lines before it was written, and it is
written from those lines, not from the walk's summary (`strm/colorspace-and-dvi.yaml:18-47`):
[8:7] digital video mode (SD:1711, Table 20); [6:5] final output terms (SD:1893, Table 23); [4]
sign or zero extension of CY/CI/CQ (SD:1863); [3], [2], [1] add DAC0 into FY, FI, FQ (SD:1878-1880,
`DAC0 & {8{CMOD[3]}}` and so on); [0] is XORed with DAC0[0] to form FS, the VGA H-Sync term
(SD:1882). The walk's "[0] sync polarity" is that XOR; the served text gives the formula's meaning,
not the label.

### PARTIAL rows on touched files

| Ledger row | SD lines confirmed | Disposition | Fix (file:line) |
|---|---|---|---|
| 1270 `setdacs.yaml` category Smart Pin (line 35) | instruction listing row 263 | REFUTED as a misfile | The instruction listing files SETDACS in its "Smart Pins" group, and `engineering/tools/p2kb-categories.json` lists `setdacs` under `smart_pin`, as the index generator accepts it. `category: Smart Pin` is kept. |
| 1272 SETDACS values overridden by the streamer and the converter (line 36) | 1268-1272 | CLOSED, fixed | `pasm2/setdacs.yaml:13-20` (background_state, with links to the streamer and converter homes); the converter side also at `strm/colorspace-and-dvi.yaml:60`. |
| 1311 command buffer and XINIT-then-XCONT idiom (line 46) | 1311 | CLOSED, fixed | `strm/overview.yaml:42-48` (command_buffer); `pasm2/xcont.yaml:44` points to it. |
| 1387-1391 ADC modes' D[22:20] (line 50) | 1387-1391; Spin2 v55 symbol templates W000 | CLOSED, fixed, two documents | `strm/modes-reference.yaml:666-670` (no_pin_field: the mode table marks them ---; Parallax's documents also give 000 in the symbol templates), the rows' `d_22_20` at `:542,560,578`; `strm/overview.yaml:139-147` (the mode table marks D[22:20] ---). |
| 1401 count 0 releases DAC overrides and pin outputs (line 52) | 1401 | CLOSED, fixed | `strm/overview.yaml:124-126` (count_field.zero); `pasm2/xinit.yaml:85` points to it. |
| 1407 XZERO waits (line 55) | 1407 | CLOSED, fixed | `pasm2/xzero.yaml:39-44` (waiting). |
| 1409 XZERO glitch with fractional NCO values (line 56) | 1409 | CLOSED, fixed | `pasm2/xzero.yaml:45-50` (fractional_frequency_glitch, with SD's own `%5555_5555 = ~1/3` as printed there; the increment-by-1 sentence moved to `strm/nco-timing.yaml:35-41`, frequency_calculation.note); `strm/nco-timing.yaml:104` points to it, and the unsourced "prevents drift accumulation" is gone. |
| 1464 imm->LUT last value repeats (line 66) | 1464 | CLOSED, fixed | `strm/modes-reference.yaml:58-67`. |
| 1472 RDFAST->LUT refill on last value (line 68) | 1472 | CLOSED, fixed | `strm/modes-reference.yaml:77-87`. |
| 1476 RDFAST->pins refill on last value (line 69) | 1476 | CLOSED, fixed | `strm/modes-reference.yaml:88-95`. |
| 1497-1509 RGBI8 colours and expansion, Table 15 (line 72) | 1497-1509 | CLOSED, fixed | `strm/modes-reference.yaml:627-637`, 8 rows. |
| 1543-1545 S[1:0] and S[1] channel select (line 76) | 1543-1547 | CLOSED, fixed | `strm/modes-reference.yaml:658-661`; the rows' `s_operand` at `:543,552,561,570,579`. |
| 1602 32-bit accumulators (line 83) | 1602 | CLOSED, fixed | `strm/dds-goertzel.yaml:91,106`. |
| 1606-1618 SINC2 accumulation formula (line 85) | 1606-1618 | CLOSED, fixed | `strm/dds-goertzel.yaml:101-119` (both SINC1 and SINC2 blocks, copied). |
| 1851 converter introduction (line 95) | 1851 | CLOSED, fixed | `strm/colorspace-and-dvi.yaml:6-11`; the `setc*` files point to it. |

### IN-PLAN row

| Ledger row | Closed against |
|---|---|
| 1214-1255 pixel formula and Table 13 (line 33) | task «#454», `language/pasm2/concepts/pixel_mixer.yaml`. Not touched here. |

### CLOSE-AGAINST

- "zero-overhead I/O operations" in `strm/overview.yaml` (unscoped, unsourced): CLOSED, fixed. The
  description at `strm/overview.yaml:24-28` is the SD:1277 introduction, and the file was certified
  whole. `grep -i "zero.overhead"` over `strm/`: none.

### Found beyond the rows (KB carve-out, fixed in this pass)

- `pasm2/concepts/streamer_smartpin_control.yaml`: the repository mode wrote its long with WYPIN
  (SD:3914: WXPIN writes it); TESTP's `Z = !pin state` (SD:1984: Z = IN); the sync serial X given as
  `clock pin<<24 | bit count` (SD:4646-4654: X[5] and X[4:0], the clock is the B input); P_NCO_FREQ's
  X and Y, P_HIGH_TICKS's X, and the quadrature reset by WYPIN (SD:4000-4014, 4165-4171, 4103).
- `pasm2/xinit.yaml` large_transfer_chunking described the flash loader's read loop as draining hub
  data to an output pin; the loader's `wmode` is a 1-pin input to hub RAM. The loop now lives in
  `code-examples/flash-loader-case-study.yaml:88-107` (large_transfer_chunking), as the one home of
  the loader's code; `pasm2/xinit.yaml:83` points to it.
- `strm/pin-selection.yaml` gave HDMI as an 8-pin mode at base 8; the SD program uses 32-pin mode
  words at a multiple-of-8 base. Its %a scope warning said X_ALT_ON does nothing in 8-bit modes; in
  the 8-pin and wider modes it sets a template bit and can select a different mode.
- `strm/dac-routing.yaml` common_configs gave X_DACS_3_2_1_0 as "R, G, B, Sync"; the RGB modes put
  0 on X0 (SD:1480).
- Derived values with no source (video pixel-rate NCO words, 48 kHz and 44.1 kHz words, NCO
  resolution) removed from `strm/nco-timing.yaml`, `pasm2/setxfrq.yaml` and `strm/dds-goertzel.yaml`.

### Sample MATCH rows re-read

| Ledger row | Result |
|---|---|
| 1416-1436 %dddd table (line 59) | MATCH. `strm/dac-routing.yaml:24-151`, 16 rows: dddd and the four channel cells agree with SD:1421-1436 row by row; descriptions now SD's own. |
| 1443-1452 %ppp pin groups (line 62) | MATCH. `strm/pin-selection.yaml:29-64` (pin_groups), 8 rows agree with SD:1445-1452. |
| 1294-1305 SETXFRQ table (line 41) | MATCH, restated. `strm/nco-timing.yaml:49-75` carries all eight SD rows in SD's own form. |
| 1586-1600 S[11:0] loop table (line 82) | MATCH. `strm/dds-goertzel.yaml` lut_window, 8 rows agree with SD:1590-1597. |
