# AN008 Sigma-delta ADC — Image Catalog

**Source:** Parallax Semiconductor AN008 v1.0 (2011), 10 pages.
**Extraction date:** 2026-06-27
**Method:** `pdftoppm -r 150` full-page renders (figures are **vector schematics** — `pdfimages` misses vector art, so page renders are the faithful capture) + `pdfimages` for the two embedded raster photos (Figure 5). Labels read directly from the clean PDF **text layer** (no OCR needed — text layer is intact, not ciphered).

## Quality gate
- All 10 page renders: clean, legible at 150 dpi.
- Two embedded photos quality-gated via `image_dominant_colors`: healthy grayscale photographs (`#303030`/`#909090` dominant — NOT `#000000`-dominant), pass. They are the **same Figure 5 photo at two resolutions** (589×589 and 400×402); the 589px copy is the higher-fidelity master.

## Figures (10 total — all schematics/diagrams except Fig 5 = photo)

| Fig | Title | Printed pg | Render | Type | Key labels (from text layer) |
|---|---|---|---|---|---|
| 1 | Inverting Operational Amplifier Circuit | 1 | `page-01.png` | schematic | 100K, 100K, Analog Input, Vdd/2 |
| 2 | CMOS D Flip-Flop | 1 | `page-01.png` | schematic | 100K, 100K, Analog Input, D, /Q, Q, Serial Digital Out, Clock |
| 3 | CTRx Register Configured for Sigma-delta Operation | 2 | `page-02.png` | bit-field diagram | "Instruction"/"Destination"/"Source" fields; bits 31..0; `01001`; Counter Mode (Positive with Feedback); Feedback Pin; Input Pin |
| 4 | Sigma-delta ADC Circuit (the standard RC network) | 3 | `page-03.png` | schematic | 1 nF, 100K, 150K, 1 nF (cap to Vdd + cap to Gnd), Counter Output, Counter Input, Analog Input |
| 5 | Typical Surface-Mount Layout | 4 | `page-04.png` + `fig05-surface-mount-layout-photo-589px.png` (master) + `...-400px.png` (dup) | **photo** | P8X32A-Q44 (1024 date code), PARALLAX; annotated Counter Input / Counter Output / Audio In; SMT passives near pins |
| 6 | Calibration Circuit for Analog Range of Vss to Vdd | 6 | `page-06.png` | schematic | R, 1 nF, 100K, 150K, 1 nF, Calibration, Counter Output, Counter Input, Analog Input |
| 7 | Analog Multiplexer | 6 | `page-06.png` | schematic | Vdd Calibrate Input, Vss Calibrate Input, 4:1 Analog MUX, Ain0..3, Aout, S0/S1, Channel Select, 1 nF, 100K, 150K, Counter Output/Input |
| 8 | Multiple Analog Inputs | 8 | `page-08.png` | schematic | Analog Input 0, Analog Input 1, two RC front-ends sharing one feedback (1 nF, 150K, 100K), Counter Input 0/1, Counter Output |
| 9 | Capacitive Coupling for Reading AC Signals | 8 | `page-08.png` | schematic | Vdd, 10K, 0.1uF, 1nF, 100K, Electret Mic, +, Counter Output, Counter Input (Propeller Demo Board mic circuit) |
| 10 | Extended Voltage Ranges | 9 | `page-09.png` | schematic | 1 nF, 100K, R1, R2, Analog Input, Counter Output, Counter Input (biasing resistors for shifted range) |

## Equations (rendered math, p.9 — `page-09.png`)
- **Eq 1a / 1b:** simultaneous summing-junction balance equations relating VHI, VLO, R1, R2, and the 100K feedback (resistances in kΩ).
- **Eq 2a:** `R1 = 100·(VHI − VLO) / 3.3  [kΩ]`
- **Eq 2b:** `R2 = 100·(VHI − VLO) / (VHI + VLO − 3.3)  [kΩ]`
  (These are transcribed from the text-layer extract, which mangles the fraction bars; the variable/constant set is reliable, the exact operator grouping should be re-verified against the page render before any downstream use — flagged as a gap.)

## Consumer references
None yet (greenfield P1 ingestion; no P2KB YAML or manual consumes these). The Figure 3 CTRx bit-field diagram and the Figure 4 standard RC circuit are the highest-value assets for the P1→P2 analog write-up (smart-pin ADC SINC mode).
