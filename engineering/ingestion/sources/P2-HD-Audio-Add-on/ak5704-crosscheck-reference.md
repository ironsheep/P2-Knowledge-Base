# AK5704 Codec Datasheet — CROSS-CHECK Evidence (🟡 NOT a primary P2 source)

**Source:** `ak5704en-en-datasheet.pdf` — AKM (Asahi Kasei Microdevices) **AK5704** "Low-Power 4-ch 32-bit ADC with MIC-Amp" · 109 pages · datasheet rev `019000890-E-01`, dated 2022/01.
**Role:** **CROSS-CHECK / corroboration only.** This is a 3rd-party component datasheet. Its contents are **NOT authoritative P2 knowledge** — they corroborate the codec facts asserted by the #64014 board guide (the primary 🏆). Do NOT promote any of this into P2KB YAML as P2 fact.
**Authority tier (proposed):** 🟡 cross-check (component datasheet; AKM).
**Extraction scope:** intentionally NOT exhaustive (109 dense pages). Only the fact-bearing fields that corroborate the board guide were pulled: part identity, pinout, audio/I²S/TDM interface, register map, key electrical/clock specs.

---

## 1. Part identity (corroborates board guide)
- **AK5704** — High-performance analog front-end AD converter; 4-ch 32-bit ADC + low-noise MIC amp; dynamic range 105 dB; built-in VAD (voice activity detection); supports up to 16-ch mic array by cascading multiple AK5704's.
- **Ordering guide (p.108):** `AK5704EN` = −40 ~ +85 °C, **28-pin QFN (0.4 mm pitch)**. `AKD5704` = AK5704 Evaluation Board.
- **Board guide says:** "Based on the AK5704EN 32-bit 4ch ADC with MIC pre-amplifier." → **MATCH** (part number, 4ch/32-bit, MIC amp, temp range).

## 2. Top-level features (datasheet §2)
- Sampling frequency 8 kHz–192 kHz. → board guide "8 k to 192 kHz" **MATCH**.
- Audio interface formats: **32/24/16-bit I²S / MSB-justified, 16-bit PCM Short/Long Frame**.
- TDM: **4-ch TDM**, **8/12/16-ch Cascade TDM**.
- Control I/F: **I²C-bus (400 kHz)**. → board guide "I2C bus (400 kHz)" **MATCH**.
- Single-ended or full-differential analog inputs; 2 digital-filter types (Low-latency [5/fs] sharp roll-off, and Voice).

## 3. AK5704 pinout (28-pin QFN) — datasheet §5.1
| Pin | Name | I/O | Function |
|---|---|---|---|
| 1 | CAD | I | I²C Chip Address Pin |
| 2 | SCL | I | I²C Serial Data Clock Pin |
| 3 | SDA | I/O | I²C Serial Data Input/Output Pin |
| 4 | WINTN | O | Interrupt Output Pin |
| 5 | SDTO1 | O | Audio Serial Data Output 1 Pin |
| 6 | TDMIN / SDTO2 | I / O | TDM Data Input (default, SDTO2E=0) **or** Audio Serial Data Output 2 (SDTO2E=1) |
| 7 | LRCK | I/O | Frame Sync Clock Pin |
| 8 | BCLK | I/O | Audio Serial Data Clock Pin |
| 9 | MCKO | O | Master Clock Output Pin |
| 10 | MCKI | I | Master Clock Input Pin |
| 11 | VDD12 | — | LDO12 (1.2 V) output (2.2 µF cap to VSS2) |
| 12 | VSS2 | — | Digital Ground |
| 13 | TVDD | — | Digital I/F & LDO12 power supply |
| 14 | PDN | I | Power-down — "L": Power-down, "H": Power-Up |
| 15 | VREF | O | Voltage Reference (2.2 µF cap to VSS1) |
| 16 | VCOM | O | Common Voltage Output (2.2 µF cap to VSS1) |
| 17 | VSS1 | — | Analog Ground |
| 18 | AVDD | — | Analog Power Supply |
| 19 | MPWR2 | O | MIC Power Supply 2 |
| 20 | AIN2B− | I | Negative Analog Input 2B |
| 21 | AIN2B+ / DMCLK2 | I/O | Positive Analog Input 2B (DMIC2=0) / Digital Mic Clock Out 2 (DMIC2=1) |
| 22 | AIN2A− | I | Negative Analog Input 2A |
| 23 | AIN2A+ / DMDAT2 | I | Positive Analog Input 2A (DMIC2=0) / Digital Mic Data In 2 (DMIC2=1) |
| 24 | AIN1B− | I | Negative Analog Input 1B |
| 25 | AIN1B+ / DMCLK1 | I/O | Positive Analog Input 1B (DMIC1=0) / Digital Mic Clock Out 1 (DMIC1=1) |
| 26 | AIN1A− | I | Negative Analog Input 1A |
| 27 | AIN1A+ / DMDAT1 | I | Positive Analog Input 1A (DMIC1=0) / Digital Mic Data In 1 (DMIC1=1) |
| 28 | MPWR1 | O | MIC Power Supply 1 |

> **Corroboration of board header signals:** every board-guide ADC header signal (SDA, SCL, SDTO2, SDTO1, LRCK, BCLK, MCKI, PDN, WINTN) maps 1:1 to an AK5704 pin of the same name and function. **MATCH.** (Board exposes a subset to the P2 accessory header; CAD/MCKO and the analog/power pins are handled on-board.)

## 4. Audio interface format (datasheet §9.5) + register 0EH
- **Register 0EH "Audio I/F Format"** bit layout: `BCKP | DLC[1:0] | TDM[1:0] | DIF[1:0]` (D6..D0; D7=0).
  - **DIF[1:0]** selects I²S vs MSB-justified vs PCM frame format.
  - **TDM[1:0]** = 00 Normal, 01 TDM128, 10 TDM256, 11 TDM512.
  - **BCKP** = BCLK polarity; **DLC[1:0]** = data length/control.
- LRCK frequency tables given for both **Slave mode** and **Master mode** (MCKO master clock out). MCKI master-clock-input timing also specified.
- → board guide's I²S signal set (MCKI/BCLK/LRCK/SDTO1/SDTO2) is exactly the datasheet's audio interface. **MATCH.**

## 5. Register map (datasheet §9.17, p.78) — key registers (corroboration index, NOT exhaustive)
| Addr | Register | Notable fields |
|---|---|---|
| 00H | Flow Control | SDTO2E, MSN, AVDDL, PSW[2:0]N |
| 01H | Power Management 1 | PMVCM, PMPLL, PMMP2/1, PMAIN2B/2A/1B/1A |
| 02H | Power Management 2 | PMDM*, PMAD2B/2A/1B/1A |
| 03H | Power Management 3 | AIRST[2:0], PMVAD, PFSDO2/1, PMPFIL2/1 |
| 04H | MIC Input & MIC Power Setting | MDIF2B..1A, AINCOM, MONON, MICL[1:0] |
| 05H | MIC Amplifier 1 Gain | MG1B[3:0], MG1A[3:0] (corroborates "+30 dB to 0 dB, 3 dB step" gain) |
| 06H | MIC Amplifier 2 Gain | MG2B[3:0], MG2A[3:0] |
| 07H | Digital MIC Setting | DCLKP2/E2, DMIC2, DCLKP1/E1, DMIC1 |
| 08H | Clock Mode Select | CM[1:0], FS[3:0] |
| 09H | PLL CLK Source Select | BCKO, MCKOE, PLS |
| 0AH–0DH | PLL Ref/FB CLK Dividers | PLD[15:0], PLM[15:0] |
| 0EH | **Audio I/F Format** | BCKP, DLC[1:0], TDM[1:0], DIF[1:0] |
| 0FH–12H | Phase Adjustment 1A/1B/2A/2B | DLYxxE, DLYxx[5:0] |
| 13H | ADC High Pass Filter | ADRST[2:0], HPF2C/1C[1:0] |
| 14H | Digital Filter Select | ADVF, VREFH, FSTHPFAD2N/1N, HPFAD2N/1N |
| 19H/1AH | Filter 1/2 Select | PFTHRx, MIXx, LPFx2/x1, HPFx2/x1 |
| 1BH–24H | VAD Setting 1–10 | VAD config (voice activity detection — corroborates "VAD feature") |
| 25H–2EH | ALC / Input Digital Volume | ALC select, IV*[7:0], REF*[7:0], ALC controls |
| 2FH–34H+ | HPF/LPF Coefficients | FH1A/FH1B/FL1A... filter coefficients |

## 6. Cross-check verdict
**Every codec-level fact stated in the #64014 board guide is corroborated by the AK5704 datasheet** — part number (AK5704EN), 4-ch/32-bit, MIC amp + gain range, 8 k–192 kHz fs, 105 dB S/N, I²C @ 400 kHz, VAD, ultrasonic capability, and the I²S signal set (MCKI/BCLK/LRCK/SDTO1/SDTO2) + I²C (SDA/SCL) + PDN/WINTN. **No conflicts found.** See `P2-HD-Audio-Add-on-extraction-audit.md` §Cross-source for the corroboration matrix.

## 7. OCR-risk / extraction caveats
- Datasheet text layer is clean (no cipher) — facts above pulled from `pdftotext -layout`, not OCR. Low OCR risk on these fields.
- Register-map bit tables were captured at index granularity only (corroboration), not every bit — intentionally non-exhaustive per task scope.
