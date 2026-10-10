# PCF8523 datasheet — reading of record (chip facts the KB uses)

**Source:** NXP Semiconductors **PCF8523 — Real-Time Clock (RTC) and calendar**, *Product data sheet*,
**Rev. 7 — 28 April 2015**, 78 pages. Held as `NO-COMMIT/PCF8523.pdf` (git-ignored, not committed);
text layer extracted 2026-10-10 with `pdftotext -layout` into `pcf8523-datasheet-text.txt` (this folder).
The title, revision and date are printed on page 1 (text file lines 2-3) and in every page footer
(`Product data sheet  Rev. 7 — 28 April 2015  N of 78`); the PDF's own metadata Title field reads
`PCF8523 Real-Time Clock (RTC) and calendar`.

**Admission:** `AUTHORITATIVE-SOURCES.md` admission route 3 (Stephen, 2026-10-10) — a chip maker's datasheet is
citable for facts about **its own chip only**: the I2C address, registers, reset values and pin behaviour of the
PCF8523. It is never a source for a claim about the Parallax #64013 board or about the P2. Which pins the
board wires, whether it carries pull-ups, and the speed the P2 driver runs are board facts and are cited to the
board guide or stay unknown.

**Extraction caveat:** the text layer is clean for tables and prose. Figures (block diagram, Fig 6, Fig 7)
are rendered with a substituted glyph map and read as noise (`DGGUHVVUHJLVWHU` = "address register"); the
figures' content is carried by the surrounding prose and tables, which are readable. Digit density
67.2% (`audit-extraction-digit-density.py`; a total-numeral-loss alarm only, not a completeness certificate).
This is a SHORT ingestion — it covers the facts the KB page uses, not all 78 pages.

| Fact the KB uses | Datasheet says | Datasheet page | Text-file lines |
|---|---|---|---|
| Identity | CMOS RTC and calendar, optimized for low power | 1 | 9-10 |
| I2C data rate | maximum 1000 kbit/s; "1 MHz Fast-mode Plus (Fm+) I2C interface, read D1h, write D0h" | 1 | 10-11, 25 |
| I2C clock modes | fSCL max 100 kHz (standard), 400 kHz (fast), 1000 kHz (Fm+); Fm+ guaranteed at 3.0 V < VDD < 5.5 V | 52 (Table 49) | 2849-2852, 2879 |
| I2C slave address | "One I2C-bus slave address (1101000) is reserved for the PCF8523" -> 7-bit $68; byte = 1101000 + R/W -> write $D0, read $D1; "other addresses can be produced on request" | 46 (Table 46) | 2583-2592 |
| I2C bus lines | SDA and SCL are "connected to a positive supply via a pull-up resistor" (a bus property; the datasheet does not say the RTC board has them) | 44 | 2449-2451 |
| Registers | 20 registers, addresses 00h-13h, auto-increment wraps from 13h to 00h | 6, 7 | 300-301, 338-340 |
| Register map | Table 6: 00h Control_1, 01h Control_2, 02h Control_3, 03h Seconds (bit 7 OS), 04h Minutes, 05h Hours (AMPM), 06h Days, 07h Weekdays (0-6), 08h Months, 09h Years (0-99), 0Ah-0Dh alarms (AEN_M/H/D/W), 0Eh Offset (MODE, OFFSET[6:0]), 0Fh Tmr_CLKOUT_ctrl, 10h Tmr_A_freq_ctrl, 11h Tmr_A_reg, 12h Tmr_B_freq_ctrl, 13h Tmr_B_reg | 7-8 | 358-403 |
| BCD | Seconds, Minutes, Hours, Days, Weekdays, Months, Years "are all coded in Binary Coded Decimal (BCD) format" | 6 (detail 19 ff.) | 312-313 (992-993) |
| Control_1 bits | CAP_SEL, T, STOP, SR, 12_24, SIE, AIE, CIE (reset values 0) | 9 (Table 7) | 418-445 |
| Software reset | "For a software reset, 01011000 (58h) must be sent to register Control_1"; "setting bits 6, 4, and 3 in register Control_1 (00h) logic 1 and all other bits logic 0" | 9 (Table 7 note 3), 12 (section 8.3) | 445, 529-533 |
| CLKOUT frequencies | COF[2:0] = 000..111 -> 32768, 16384, 8192, 4096, 1024, 32, 1 Hz, disabled (high-Z); default 32768 | 33 (Table 35) | 1756-1768 |
| INT1/CLKOUT pin | one pin carries INT1 and CLKOUT, "open-drain"; "can either drive the CLKOUT or the INT1" | 5 (Table 5), 32 | 272-273, 280, 1734-1736 |
| Backup current | typical 150 nA at VDD = 3.0 V, Tamb = 25 C | 1 | 24 |

## Not stated by this datasheet (so not citable from it)
- Which logic level / wiring the #64013 board gives any pin, and whether the board carries SDA/SCL pull-ups.
- The speed or pull-up setting any Parallax driver uses.
