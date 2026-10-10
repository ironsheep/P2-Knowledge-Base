# AK5704 datasheet — reading of record (chip facts the KB uses)

**Source:** Asahi Kasei Microdevices (AKM) **AK5704 — Low-Power 4-ch 32-bit ADC with MIC-Amp**,
document number **019000890-E-01**, dated **2022/01**, **Rev.1** (printed `Rev.1` on the last page, revision 01
dated 22/01/31 in the Revision History), 109 pages. Held as `ak5704en-en-datasheet.pdf` (git-ignored); text
layer extracted 2026-10-10 with `pdftotext -layout` into `ak5704-datasheet-text.txt` (this folder). Printed page
numbers (`- N -`) equal PDF page numbers. Title: page 1 (text lines 6-7); document number and date: every page
footer (line 57 etc.); revision: lines 6553-6555 (page 108) and 6619 (page 109).

This SUPERSEDES the standing of the earlier `ak5704-crosscheck-reference.md` (a cross-check capture, frozen as
written): the datasheet is now admitted by `AUTHORITATIVE-SOURCES.md` admission route 3 (Stephen, 2026-10-10) for
facts about **its own chip only** — the I2C address, registers, reset values, pin behaviour of the AK5704 — and
never for a claim about the Parallax #64014 board or the P2. Which level the board ties CAD to, what the board
wires to the P2, and whether the board carries pull-ups are board facts: the board guide or unknown.

**Extraction caveat:** text layer clean. SHORT ingestion: the facts the KB page uses, not all 109 pages. Digit
density 85.0% (`audit-extraction-digit-density.py`; total-numeral-loss alarm only).

| Fact the KB uses | Datasheet says | Datasheet page | Text-file lines |
|---|---|---|---|
| Identity | "Low-Power 4-ch 32-bit ADC with MIC-Amp"; 4-ch 32-bit ADC, MIC amp gain +30 dB to 0 dB in 3 dB steps, S/N and DR 105 dB, 28-pin QFN, fs 8 k to 192 kHz | 1 | 6-52 |
| I2C clock | "Control I/F: I2C-bus (400kHz)"; "fast-mode I2C Bus (max: 400kHz)". "Pull-up resistors at the SDA and SCL pins must be connected to (TVDD+0.3)V or less" (a bus requirement; says nothing of any board) | 1, 75 | 47, 4432-4433 |
| CAD pin | pin 1, input, "I2C Chip Address Pin" | 6 (5.2) | 305 |
| I2C slave address | first byte = `0 0 1 0 0 0 CAD R/W`; "The most significant six bits of the slave address are fixed as 001000"; "CAD must match with CAD pin" -> 7-bit address %001000C: **$10 with CAD = 0 (write $20, read $21)**, **$11 with CAD = 1 (write $22, read $23)** | 75, 76 (Fig 48) | 4439-4441, 4485-4486 |
| Register range | register map 00H-46H; address counter rolls over to 00H after 46H; "Writing access to 47H ~ 7FH is prohibited"; register values initialised by PDN = L | 75, 76, 78-79 | 4457-4458, 4501-4502, 4633-4721 |
| Register groups | 00H Flow Control, 01H-03H Power Management, 04H MIC input & power, 05H-06H MIC gain, 07H digital mic, 08H Clock Mode Select, 09H-0DH PLL, 0EH Audio I/F Format, 0FH-12H phase adjustment, 13H-14H HPF / filter select, 15H-18H MIC sensitivity, 19H-1AH filter select, 1BH-24H VAD, 25H-2EH ALC and input volume, 2FH-46H filter coefficients | 78-79 | 4634-4718 |
| SDTO2 default | pin 6 is "TDM Data Input Pin (Default) (SDTO2E bit = 0)" and "Audio Serial Data Output 2 Pin (SDTO2E bit = 1)"; register 00H bit D6 SDTO2E, default 0: "Disable (TDMIN pin: Default)", 1: "Enable (SDTO2 pin)" | 6 (5.2), 80 | 319-325, 4751-4753 |
| Audio formats | 32/24/16-bit I2S/MSB justified, 16-bit PCM short/long frame, 4-ch TDM, 8/12/16-ch cascade TDM; master/slave | 1 | 37-45 |
| WINTN | pin 4, output, "Interrupt Output Pin" | 6 | 314 |

## Not stated by this datasheet (so not citable from it)
- The level the #64014 board ties CAD to (so which of $10 / $11 the board answers at is not recoverable here).
- That the #64014 board carries SDA/SCL pull-ups, or what the board wires to SDTO2's pad.
- Any Parallax driver's device-ID constant.
