# P1 Propeller Manual v1.2 — Image Catalog (Pass 3)

**Source:** `P1 P8X32A-Web-PropellerManual-v1.2.pdf` (399 pp) · **Extracted:** 2026-06-22
**Method (tool-proving result):** `pdfimages` found only **7 unique rasters** out of 163 objects
(73× a decorative "IMPROVED" badge + masks) — **the manual's figures are vector line-art**, so the
image pass used **`pdftoppm` page-render (200 dpi) → PIL crop → `image-tools-mcp` OCR/quality-gate**,
NOT raster XObject extraction. All 14 figures pass the brightness/ink quality gate (no black/failed
captures). Crop source pages retained in `page-renders/`.

> **Methodology note routed to Pass 7:** for diagram-heavy P1/P2 source PDFs, `pdfimages`/PyMuPDF
> raster extraction is the *wrong default* — it silently misses vector figures. Page-render+crop is
> the correct figure workflow. (image-extraction-methodology.md still assumes raster-first.)

## Figures (14)

| ID | File | Pg | Type | Content / OCR'd labels | Consumers |
|----|------|----|------|------------------------|-----------|
| 1-1 | `fig-1-1-example-wiring-diagram.png` | 17 | schematic | Example wiring: host + EEPROM access to Propeller (P30/P31 serial, P28/P29 EEPROM, regulator, reset) | hardware/boot YAML; P1 hookup docs |
| 1-2 | `fig-1-2-block-diagram.png` | 20 | **architecture** | **Propeller Chip Block Diagram.** 8 cogs (0–7; drawing shows 0–4) each = Counter A+PLL, Counter B+PLL, Video Generator, I/O Output Reg, I/O Direction Reg, **512×32 RAM**, Processor; wired-OR I/O onto 32/32/32/16 buses; **Hub** = Bus Sequencer, **8192×32 RAM**, **8192×32 ROM**, **Cog Enables**, **Lock Bits (8)**, Configuration Register; clock system = Power-Up Detector (~10 ms), Reset Delay (250 ms), Brown-Out Detector, RC Oscillator 12 MHz/20 kHz, Clock PLL MUX (1×,2×,4×,8×,16×; 16× ⇒ 64–128 MHz), Crystal Oscillator (4–8 MHz w/ PLL → DC–80 MHz), Clock Selector; signals RESET, CLKSEL, CLOCK, SOFTRES, PLLENA, OSCENA, OSCMODE | architecture/* YAML (cog, hub, clock); P1↔P2 comparison |
| 1-3 | `fig-1-3-cog-hub-best-case.png` | 25 | timing | Cog-Hub Interaction **Best Case**: System Clock falling-edge #0–24, Cog Clock, Hub Clock, Cog w/Hub Access (round-robin 0–7→0), Cog 0 Hub Instruction (HI) takes **8 clocks** when window aligned | architecture/hub timing |
| 1-4 | `fig-1-4-cog-hub-worst-case.png` | 25 | timing | Cog-Hub Interaction **Worst Case**: HI **missed, waiting to sync (15 clocks)** + execute (8 clocks) = **23 clocks** total | architecture/hub timing |
| 1-5 | `fig-1-5-main-ram-map.png` | 31 | memory map | **Main Memory Map.** RAM $0000–$7FFF (Propeller Application Code & Data, 8192 longs); ROM $8000–$FFFF: Character Set $8000–$BFFF (4096 longs, 256 chars × 16×32), Anti-Log/Log Table $C000–$D7FF (2048 words), Sine Table $E000–$F001 (2049 words), Boot Loader & Spin Interpreter $F002–$FFFF | architecture/memory YAML; ROM-contents |
| 1-6 | `fig-1-6-propeller-font-characters.png` | 32 | chart | Propeller Font Characters — the 256-character ROM font grid | reference/character-set |
| 1-7 | `fig-1-7-character-interleaving.png` | 33 | bitmap | Propeller Character Interleaving — how two 16×32 chars pack into longs (this is one of the 7 genuine rasters: `images-raw/p1img-033-023.png`, 251 KB) | reference/character-set |
| 1-8 | `fig-1-8-button-3d-beveled.png` | 33 | bitmap | "Run" button with 3-D beveled edges (Propeller Font example) | reference/character-set |
| 2-1 | `fig-2-1-byte-memory-addressing.png` | 54 | diagram | Main Memory **Byte**-Sized Data Structure and Addressing | language/spin1 BYTE |
| 2-2 | `fig-2-2-long-memory-addressing.png` | 131 | diagram | Main Memory **Long**-Sized Data Structure and Addressing | language/spin1 LONG |
| 2-3 | `fig-2-3-fixed-delay-timing.png` | 220 | timing | Fixed Delay Timing (WAITCNT example output) | language/spin1 WAITCNT |
| 2-4 | `fig-2-4-synchronized-delay-timing.png` | 221 | timing | Synchronized Delay Timing (WAITCNT periodic loop) | language/spin1 WAITCNT |
| 2-5 | `fig-2-5-word-memory-addressing.png` | 230 | diagram | Main Memory **Word**-Sized Data Structure and Addressing | language/spin1 WORD |
| 3-1 | `fig-3-1-runtime-call-procedure.png` | 269 | diagram | Run-time CALL Procedure (PASM1 CALL/RET mechanism, return-address self-modify) | language/pasm1 CALL |

## Quality gate (all PASS)
All 14 crops: mean luminance 220–247, %white-background 73–95%, ink 3–11%. No `#000000`-dominant /
full-page mis-captures (the v3.0 failure class is eliminated by DOCX-media/page-render sourcing).

## Image-enhancement debt
- **Figs 1-3, 1-4** (p25 stacked timing diagrams): crops are content-complete but bounding could be
  tightened (1-3 includes a sliver of page header; 1-4 omits its repeated top clock rows). Backstop:
  full page `page-renders/pg-025.png`. Low priority.
- Cog-internal micro-labels in Fig 1-2 are below OCR legibility at 200 dpi (illegible in the original
  too); the architectural block labels all OCR cleanly. Re-render at 300 dpi only if a consumer needs them.
