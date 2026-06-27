# P2 HD Audio Add-on Set (#64014) — Complete Reference (PRIMARY 🏆)

**Source:** `64014-P2-HD-Audio-Add-on-Set-Guide.pdf` (Parallax Inc.) · 6 pages
**Doc version:** v1.0, 10/26/2022 (footer also shows 10/16/2022 on p.1) · "Version 1.0: Original release."
**Authority tier (proposed):** 🏆 PRIMARY (Parallax product guide — authoritative for the P2 add-on board)
**Ingestion mode:** new / greenfield · passes 1–5 (stage-only)

> Cross-check companion: `ak5704-crosscheck-reference.md` (AKM AK5704 codec datasheet, 🟡 cross-check tier — NOT a primary P2 source). Used only to corroborate the codec facts the board guide states.

---

## 1. Product overview

The **P2 HD Audio Add-on Set (#64014)** is a two-board kit:

- **ADC board** — 4-channel, 32-bit, 192 kHz Audio ADC (Analog-to-Digital Converter), based on the **AKM AK5704EN** codec.
- **DAC board** — 2-channel, 16-bit, 18–990 ohm Audio DAC (Digital-to-Analog Converter), built directly on **P2 Smart Pin DAC modes** (no dedicated codec chip).

Both boards use a **standard 2x6-way (2x6-pin) 0.1" pitch female passthrough socket**, compatible with any standard single Parallax P2 accessory socket on most P2 development boards. Designed to fit side-by-side at a dual port. Usable with any 3.3 V-signal-level microcontroller.

- ADC: 4 input channels via two stereo 3.5 mm jack sockets, or two sets of unpopulated 0.1" 3-way header pads.
- DAC: 2 output channels via one stereo 3.5 mm jack socket, or unpopulated 0.1" 3-way header pads.
- Jack sockets usable in mono or stereo modes (independent L/R or stereo pair).

Target applications: robotics, interactive displays, conferencing, stadium, studio, industrial audio.

---

## 2. ADC board — AK5704EN

### Features
- Based on the **AK5704EN** 32-bit 4ch ADC with MIC pre-amplifier.
- High-performance analog front-end A/D converter, ideal for voice recognition, voice control, conferencing.
- Superior low-noise recording with low power consumption.
- **VAD (voice activity detection)** to further reduce system power.
- Supports **ultrasonic recording**.
- Sampling frequency **8 kHz to 192 kHz**.
- MIC input jack configurable for line-level signals — up to 4 channels of line input.
- MIC input channels have configurable voltage pull-up for analog microphones.
- 2x6 female socket, 0.1" spacing, Parallax P2 Accessory-socket compatible.

### Key specifications
| Spec | Value |
|---|---|
| Supply voltage | +3.3 VDC |
| Control interface | **I²C bus (400 kHz)** |
| Max bits | 32 bit |
| Max fs | 192 kHz (typical 48 kHz) |
| Max S/N | 105 dB |
| MIC amplifier gain | +30 dB to 0 dB, 3 dB step |
| Form factor | dual 2x6-pin female passthrough headers, 0.1" spacing |
| Mounting hole | 3.2 mm diameter |
| Operating temperature | −40 to +185 °F (−40 to +85 °C) |
| PCB dimensions | 1.6 x 1 in (40.64 x 25.4 mm) |

### ADC board pin connections (accessory header → ADC function)
| Accessory header pin | ADC function | Description |
|---|---|---|
| VIO3V3 | 3V3 | Supply voltage — 3.3 V required to power the ADC board |
| +7 | SDA | I²C Serial Data Input/Output Pin |
| +6 | SCL | I²C Serial Data Clock Pin |
| +5 | SDTO2 | Audio Serial Data Output 2 Pin (audio from Line input jack) |
| +4 | SDTO1 | Audio Serial Data Output 1 Pin (audio from MIC input jack) |
| +3 | LRCK | Frame Sync Clock Pin |
| +2 | BCLK | Audio Serial Data Clock Pin |
| +1 | MCKI | Master Clock Input Pin |
| +0 | PDN | Power-down Pin — "L": Power-down, "H": Power-Up |
| GND | GND | Common Ground reference connection |
| N/C | WINTN | Interrupt Output Pin (customer option — unpopulated header) |

> Guide note: "Refer to the AK5704EN ADC datasheet for full details, available from www.akm.com." (This is the cross-check companion datasheet.)

**I²S/audio wiring summary (ADC):** MCKI (master clock in), BCLK (bit clock), LRCK (frame/word-select), two serial data outputs SDTO1 (MIC) + SDTO2 (Line). I²C (SDA/SCL) for register control. PDN power-down, WINTN interrupt (unpopulated).

---

## 3. DAC board — P2 Smart Pin DAC

### Features
- Designed to leverage the **Parallax P2 Smart Pin DAC modes** (no codec IC — the P2 pins are the DAC).
- Configurable drive strengths from **18 to 990 ohms**.
- High-performance output for announcements, music, general sound monitoring/reproduction.
- Superior low-noise output, low power.
- 2x6 female socket, 0.1" spacing, P2 Accessory-socket compatible.

### Key specifications
| Spec | Value |
|---|---|
| Supply voltage | +3.3 VDC |
| Vpp output | 2 V or 3 V configurable |
| Drive impedance | 18.75 ohms to 990 ohms, configurable in 16 steps |
| Form factor | dual 2x6-pin female pass-through headers, 0.1" spacing |
| Mounting hole | 3.2 mm diameter |
| Operating temperature | −40 to +185 °F (−40 to +85 °C) |
| PCB dimensions | 1.6 x 1 in (40.64 x 25.4 mm) |

### DAC board pin connections (accessory header → DAC function)
> The source table merges cells with explanatory text; reconstructed faithfully from the layout extract (`P2-HD-Audio-Add-on-text.txt` lines 135–169).

| Accessory header pin | DAC function | Description |
|---|---|---|
| VIO3V3 | N/C | Not Connected |
| +7 | DAC_L | Common DAC Left Channel inputs (wired in parallel) |
| +6 | DAC_L | (same L channel) |
| +5 | DAC_L | (same L channel) |
| +4 | DAC_L | (same L channel) |
| +3 | DAC_R | Common DAC Right Channel inputs (wired in parallel) |
| +2 | DAC_R | (same R channel) |
| +1 | DAC_R | (same R channel) |
| +0 | DAC_R | (same R channel) |
| GND | GND | Common Ground reference connection |

**DAC drive-strength design notes (verbatim intent):**
- Drive line-level or headphone-level devices by using 1, 2, 3, or 4 channels simultaneously to set the required output drive impedance and max Vpp.
- Each P2 Smart Pin can output with these options:
  - 990 ohms, 3.3 V peak
  - 600 ohms, 2.0 V peak
  - 123.75 ohms, 3.3 V peak
  - 75 ohms, 2.0 V peak
- **Example:** For ~31 ohms drive (common for headphones), set the **123.75 ohms** mode on **4 channels** and use Ohm's law: total output impedance = 123.75 / 4 = **30.9375 ohms**. With this setting you can plug headphones directly into the DAC board's audio jack.
- Left and Right channels each combine 4 paralleled Smart-Pin outputs (pins +7..+4 = Left, +3..+0 = Right).

---

## 4. Board dimensions / mechanical
- Both PCBs: **1.6 x 1 in (40.64 x 25.4 mm)**, 3.2 mm mounting hole.
- Mechanical dimension drawings appear on the ADC (p.3–4) and DAC (p.6) pages — see `assets/images-P2-HD-Audio-Add-on-2026-06-27/image-catalog.md`.

## 5. Resources and downloads
"Check for the latest version of this document, schematics and example code from the P2 HD Audio Add-on Set product page. Go to www.parallax.com and search for 64014."

> **No code is embedded in this guide** — example code lives on the product page only. Pass-2 code count = 0 (nothing to extract/validate).

## 6. Revision history
- **Version 1.0:** Original release. (10/26/2022)

---

## Codec / interface identity (captured cleanly, per handback ask)
- **Codec part:** AKM **AK5704EN** (28-pin QFN per datasheet) — ADC board only. DAC board has **no codec** (P2 Smart Pin DACs).
- **I²S/TDM wiring (ADC):** MCKI / BCLK / LRCK / SDTO1 (MIC) / SDTO2 (Line). I²C control = SDA/SCL @ 400 kHz. PDN power-down; WINTN interrupt (unpopulated).
- **DAC wiring:** 4 paralleled P2 Smart-Pin outputs per channel — DAC_L (header +7..+4), DAC_R (header +3..+0); driven entirely by P2 Smart Pin DAC modes.
