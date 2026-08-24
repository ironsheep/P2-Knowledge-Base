# P2 Eval Board Rev C Complete Extraction Audit

**Document**: 64000 Propeller 2 Eval Board Rev C Guide.pdf
**Version**: v2.0 (29/6/2020)
**Date**: 29/6/2020
**Pages**: 17
**File Size**: 4.9MB
**Extraction Date**: **2026-08-24 (forced-OCR RE-EXTRACTION)** · prior capture 2025-08-29 (lossy — archived)
**Trust Level**: ✅ GREEN (Official Parallax hardware documentation)

---

## ⚠️ RE-EXTRACTION NOTICE (2026-08-24) — F-250

> **The 2025 extraction of this source lost every numeral.** The #64000 PDF's body font does
> not map numerals, so `pdftotext` returned the prose with each digit silently deleted — the
> shipped `p2-eval-board-narrative.txt` carried a digit on **91 of 1315 lines (10.0% of
> non-blank lines)**, against a measured peer band of **29–58%** across eleven other
> board/hardware sources. Lines read *"The Propeller has cores, KB of hub RAM, and Smart I/O
> pins"*. **This document's earlier "100%" coverage claim was false** and is corrected below.
>
> **Repaired 2026-08-24** by `pdf-ocr --force-ocr --deskew` → `pdftotext -layout`, giving
> **303 of 576 non-blank lines carrying a digit (52.6%)** — inside the peer band (on the
> gate tool's own ≥12-char metric, **1.5% → 56.5%**). The two
> ruled tables were re-cut with `camelot lattice`, and **every one of the 17 pages was read
> against its rendered page image**; the numeral-bearing pages all matched.
>
> Caveat carried forward: **digit density is a smoke alarm, not a certificate.** It detects
> *total* numeral loss, never partial. Passing it is not evidence that a source is complete.
>
> - Prior artifacts: `archive/` (see `archive/README.md`).
> - Curated source of record: `complete-p2-eval-board-reference.md`.
> - Raw layout extract of record: `p2-eval-board-text.txt`.
> - Register trace: `engineering/operations/P2KB-CORRECTION-FINDINGS.md`
>   **F-250** (`PARTIAL` — ingestion half complete 2026-08-24, `:360`) and
>   **F-328** (`CONFIRMED` — the board YAML half it exposed, `:65`).

---

## 📁 EXTRACTED ASSETS

### 🖼️ Image Catalog
**[Complete Image Catalog: assets/images-20250829/image-catalog.md](assets/images-20250829/image-catalog.md)**
- **Total Images**: 15 (board photos, configuration diagrams, technical schematics, pinout reference)
- **Extraction Date**: 2025-08-29
- **Success Rate**: 100% (15/15 images successfully extracted)
- **Key Visual Assets**: High-resolution board photographs, feature identification diagrams, power configuration details, I/O pin breakout specifications, mechanical PCB dimensions
- **Usage**: Hardware setup guides, pin configuration reference, power system documentation, mechanical design specifications

---

## 📊 EXTRACTION SUMMARY
### Document Type & Purpose
Official hardware guide for P2 Eval Board Rev C (#64000) - production-approved engineering evaluation platform. Provides complete specifications, feature descriptions, pin assignments, and operational guidelines for P2 development work.

### Key Distinguishing Features
- **Production-ready Rev C silicon** (P2X8C4M64P) - final engineering sample
- **Complete hardware implementation** - power, programming, I/O, expansion
- **Practical development platform** - enables real P2 code testing and validation
- **Accessory ecosystem integration** - 2x6 edge headers for expansion boards

## 🔍 CONTENT INVENTORY
### Core Technical Specifications
_Re-verified 2026-08-24 against the OCR'd text ∩ camelot tables ∩ rendered pages. Verdict per
line below; the full triple-validated capture is `complete-p2-eval-board-reference.md`._

- **Microcontroller**: **P2X8C4M64PES** (8 cogs, 512 KB hub RAM, 64 smart pins) — ✅ figures
  verified; **part number CORRECTED** (was `P2X8C4M64P`). p.2 key spec and the p.4 diagram
  callout read `P2X8C4M64PES`; the p.4 heading, the p.3 bullet and the board silkscreen read
  `P2X8C4M64P`. Both strings are in the source.
- **Clock System**: 20 MHz crystal, adjustable, recommended maximum 180 MHz; overclocking
  possible beyond 300 MHz — ✅ verified; **add** the §8 datum *"early unsupported experiments
  have been running the Propeller 2 overclocked at 390 MHz without significant heat rise"*.
- **Memory**: 16 MB (128 Mbit) SPI Flash (W25Q128JVSIM) — ✅ verified (p.2, §17).
- **I/O**: 64 Smart I/O pins — the source states **both** "64 accessible, **58 fully free**"
  (p.2, twice) and "**P0–P55 are fully free**; P56–P63 are routed to peripheral circuits"
  (p.15). §12 adds a third statement: "P56 and P57 are free by default". *(Observation, not the
  source's: 56 + 2 = 58 would reconcile them — the guide never says so.)* ⚠️ carry
  both, in the source's wording — do not compute one number.
- **Power**: Dual micro-USB (PC-USB 500 mA, AUX-USB 2000 mA), 1.8 V / 2 A VDD switching buck
  regulator (1 MHz nominal), 3.3 V LDO regulators (300 mA per 8-pin group) — ✅ verified.
- **Programming**: Built-in FTDI USB serial interface; serial over micro-USB, user selectable
  up to 3 Mbps — ✅ verified.
- **Storage**: MicroSD card socket (P58–P61 hardwired) — ✅ pins verified; ⚠️ the source
  **contradicts itself on P58/P59 direction** (§18 bullets vs the p.15 table) → **F-328**.
- **Physical**: 3.55" x 3.55" PCB, four mounting holes spaced 40 mm apart — ✅ verified. The
  source's own metric parenthetical reads "(90 x 90 cm)", which is a **source typo** (3.55 in
  = 90 mm); quote the inch figure.
- **Thermal / mechanical (was missing)**: continuous 4 oz copper ground plane on the bottom
  layer; the 40 mm hole spacing "could accommodate a 50 mm fan or heatsink" (§8).
- **Absolute maxima (was missing)**: USB input absolute maximum 5.5 VDC; AUX pads input range
  4.5–5.5 V; **absolute maximum P2 VDD 2.2 V**; brown-out holds the P2 in reset below ~1.5 V.
- **Operating temperature (was missing)**: −40 to +185 °F (−40 to +85 °C).

### Part Numbers Catalog
- **#64000** - P2 Eval Board Rev C (primary part number)
- **#64006-ES(b)** - USB accessory requiring 5V supply
- **#32420S** - WX WiFi SIP Module for wireless programming

### Hardware Features Breakdown
- **20 numbered feature callouts** with detailed descriptions
- **Complete pin assignment tables** (P0-P63 with alternative functions)
- **Boot mode selection matrix** (6 different boot configurations)
- **Power system architecture** (USB logic, VDD supply, LDO regulators)
- **Edge header specifications** (8 sets of 2x6 headers with voltage options)

### Rev C Specific Improvements
- Production-approved P2X8C4M64P silicon
- Trace-length matching for high-speed data (P0-P15, P32-P47)
- Permanent brownout detection connection
- USB reset switch control
- Pin assignment changes (5V pins removed/relocated)
- Enhanced USB power circuit protection
- WX WiFi compatibility (P56-P63 header)

## 📋 STYLE ANALYSIS
### Document Architecture
Standard Parallax technical documentation format:
- Executive overview with key specifications
- "What's New" revision summary
- Numbered feature descriptions with detailed explanations
- Complete pin assignment reference tables
- Physical specifications and mounting details

### Content Patterns
- **Feature-driven organization** - each major component gets dedicated section
- **Practical implementation focus** - emphasizes how to use, not just what it is
- **Cross-reference integration** - links to related documentation (Silicon Doc, Google Docs)
- **Safety warnings** - highlighted cautions for voltage limits and connections
- **Visual documentation** - board photos, diagrams, pin layouts

### Voice & Tone
Professional technical documentation with practical development focus. Assumes engineering audience familiar with microcontroller concepts but provides sufficient detail for implementation decisions.

## 🔄 CROSS-SOURCE VALIDATION RESULTS

### Pass 1: Questions Answered from Previous Sources

#### From Silicon Doc Gaps:
✅ **Q**: What are the physical specifications and power requirements for P2 development?
**A**: #64000 provides complete implementation - 3.55"x3.55" PCB, dual USB power (500mA/2000mA), 1.8V/2A VDD, distributed 3.3V LDOs
**Source**: Pages 2-3, 6-7
**Confidence**: High

✅ **Q**: How do you actually program and interface with P2 hardware?
**A**: Built-in FTDI USB interface, multiple boot modes (serial/flash/SD), complete I/O breakout via 2x6 edge headers
**Source**: Pages 5, 11-12, 15-16
**Confidence**: High

✅ **Q**: What development ecosystem exists for P2 expansion?
**A**: 8 sets of 2x6 pass-through headers accommodate accessory boards (#64006-ES(b) example), WX WiFi module (#32420S) support
**Source**: Pages 9-10, references throughout
**Confidence**: High

#### From SPIN2/PASM2 Documentation Gaps:
✅ **Q**: What hardware platform enables testing SPIN2/PASM2 code?
**A**: #64000 provides production-ready P2 platform with complete programming interface and I/O access
**Source**: Complete document scope
**Confidence**: High

### Pass 2: New Questions Raised

#### Hardware Design:
1. **What cooling solutions are compatible with the 40mm mounting holes?** - Enables overclocking experimentation beyond 300MHz
2. **How do distributed 3.3V LDO regulators improve analog performance compared to single switcher?** - Critical for precision analog applications
3. **What specific accessory boards exist for the 2x6 header ecosystem?** - Determines expansion capabilities

#### Software/Firmware:
4. **What PNUT P2 programming software versions are required for Rev C silicon?** - v34s+ recommended but evolution continues
5. **How does brownout detection at 1.5V threshold affect application reset behavior?** - Important for power supply design

#### Integration/Ecosystem:
6. **What trace-length matching specifications enable high-speed data experiments?** - HyperRAM and similar applications
7. **How does WX WiFi module integration work with P56-P63 header?** - Wireless programming workflow

### Pass 3: Conflicts Identified
⚠️ **No Direct Conflicts** with existing P2 documentation - This document provides hardware implementation details that complement rather than contradict Silicon Documentation and language references. All core P2 specifications (8 cogs, 512KB hub RAM, 64 smart pins, clock ranges) match established documentation perfectly.

**Re-extraction pass, 2026-08-24 — conflicts the digit-free capture could not see:**

*Internal to the source* (the guide contradicting itself; verified on the rendered pages, not
extraction defects):
1. **microSD P58/P59 direction.** §18 (p.12) lists P58 = DI/CD (data in), P59 = DO (data out);
   the p.15 alternative-function table lists P58 = microSD MISO (SDO), P59 = microSD MOSI (SDI).
   P60/P61 agree. The guide does not resolve it. → **F-328**.
2. **"58 fully free" (p.2, twice) vs "P0–P55 are fully free" (p.15).**
3. **"3.55″ × 3.55″ (90 x 90 cm)"** — the metric parenthetical is a source typo (90 mm).
4. **Document version string** — page footers read "v2.0 29/6/2020"; the p.17 Revision History
   reads "Version 3.0".
5. **Chip part number** — `P2X8C4M64PES` (p.2, p.4 callout) vs `P2X8C4M64P` (p.3, p.4 heading,
   silkscreen).
6. **Referenced Google Document** — §8 says "(Rev B Silicon)"; §1/p.14/p.15 say "(Rev B/C Silicon)".

*Against the published P2KB* — the board YAML carries claims this source contradicts or does not
contain. Routed to the corrections register as **F-328**; not fixed here (this folder produces
raw source data only).

### Pass 4: Content Contribution Audit
**vs Silicon Doc**: Provides complete physical implementation, power requirements, pin access, and development workflow that Silicon Doc hardware abstraction doesn't cover
**vs SPIN2/PASM2 Manuals**: Enables actual code deployment, testing, and hardware interaction - bridges from language concepts to working systems
**vs Smart Pins Analysis**: Provides the physical platform needed to test smart pin configurations in real hardware with proper I/O access
**vs Edge Module Documentation**: Establishes evaluation/prototyping platform that complements production Edge modules

### Pass 5: Cross-Reference Validation
- **P2X8C4M64P silicon specifications** cross-verified with Silicon Doc ✓
- **Smart I/O pin capabilities** match Silicon Doc smart pin descriptions ✓  
- **Boot sequence options** consistent with established P2 boot ROM behavior ✓
- **Clock frequency ranges** (20MHz crystal, 180MHz recommended, 300+ overclocking) align with Silicon Doc specifications ✓
- **Hub RAM (512KB) and cog count (8)** match all established P2 documentation ✓

## 🎯 KNOWLEDGE BASE INTEGRATION
### Unique Value Contribution
This document fills the critical gap between P2 theoretical capabilities and practical implementation. While we have comprehensive Silicon Documentation and language references, this provides the essential hardware platform knowledge needed to:

1. **Enable Physical Development** - Complete specifications for actual P2 code testing
2. **Bridge Theory to Practice** - Shows how to connect, power, and program real P2 systems
3. **Support Hardware Integration** - Pin assignments, power requirements, expansion options
4. **Enable Ecosystem Understanding** - Accessory boards, programming options, development workflow

### Integration Recommendations
- **Cross-link with Silicon Doc** for hardware/software correspondence
- **Reference from SPIN2/PASM2 examples** when showing deployment
- **Connect to Smart Pins documentation** for I/O implementation examples
- **Link hardware specifications** to code performance characteristics

### Technical Debt Generated
- ~~**Image Extraction Needed**~~ — **CLEARED**: 15 images extracted + catalogued 2025-08-29
  (`assets/images-20250829/image-catalog.md`). The line was already stale when written.
- **Part Number Cross-Reference**: Build #64000 ecosystem map with related accessories
- **Development Workflow Documentation**: Connect hardware setup to programming tool chain

## 🔍 EXTRACTION COMPLETENESS ASSESSMENT

> **The block below replaces a false "100% across the board" claim.** That claim stood while the
> shipped extraction contained no numerals at all — no pin number, no voltage, no capacity. A
> status line is not evidence. Each figure below names the artifact it was measured on.

### Digit density — the instrument this source's failure produced

**Two metrics, both stated, because they are not interchangeable.** The tool counts only lines
of **≥12 characters** (page furniture and one-word lines are noise in both directions); the
F-250 filing counted every **non-blank** line. Same artifacts, same verdict, different
denominators — quote the metric with the number.

| Artifact | metric | lines | with a digit | density |
|---|---|---|---|---|
| `archive/p2-eval-board-narrative.txt` (2025, shipped) | tool (≥12 chars) | 399 | 6 | **1.5%** ❌ |
| `p2-eval-board-text.txt` (2026-08-24, forced OCR) | tool (≥12 chars) | 499 | 282 | **56.5%** ✅ |
| `archive/p2-eval-board-narrative.txt` | non-blank | 908 | 91 | 10.0% ❌ |
| `p2-eval-board-text.txt` | non-blank | 576 | 303 | 52.6% ✅ |

Peer band measured across eleven other board/hardware sources at tasking, on the **non-blank**
metric: **29–58%** (`p2-hardware-manual` 29 · `p2-universal-motor-driver` 30 · `p2-datasheet` 31 ·
`parallax-wx-wifi` 32 · `propplug-rev-e` 36 · `p2-microSD-addon` 40 · `p2-eval-add-on-boards` 44 ·
`p2-wx-adapter` 45 · `hyperRam-n-hyperFlash` 48 · `P2-RTC-Add-on` 57 · `P2-HD-Audio-Add-on` 58).
On the **tool** metric the same peers run ~40–71%. Either way `p2-eval-board` was the single
outlier, by an order of magnitude. **That is not a clean bill of health for the other eleven** —
digit density catches *total* numeral loss, never partial.

Check it yourself — the tool metric:
`python3 engineering/tools/validation/audit-extraction-digit-density.py engineering/ingestion/sources/p2-eval-board`
and the negative control, which must exit 1:
`python3 engineering/tools/validation/audit-extraction-digit-density.py engineering/ingestion/sources/p2-eval-board/archive/p2-eval-board-narrative.txt`

### Coverage — measured 2026-08-24, not asserted

| Area | Coverage | How it was established |
|---|---|---|
| Hardware specifications (p.2 key specs) | **complete** | OCR text ∩ rendered p.2 — every row matched |
| Feature descriptions | **complete — 20 of 20** | OCR text ∩ rendered pp.4–13 (callout diagram lists 1–20; all 20 sections present) |
| Pin assignments (P0–P63 + alternative functions) | **complete** | `camelot lattice` p.15/p.16 ∩ OCR ∩ rendered pages ∩ the p.14 physical-pin diagram |
| Edge-header pin *order* | **complete** | figure-read only (pp.9, 10, 17) — it exists in no text layer |
| Power system | **complete** | OCR ∩ rendered pp.5–8 |
| Boot options | **complete — 6 of 6 rows** | `camelot lattice` p.12 ∩ OCR ∩ rendered p.12. Column headers are **P59 △ / P59 ▽** (triangles); OCR reads them as "A"/"V" — the rendered page and the p.17 silkscreen both show triangles |
| Physical specifications | **complete for the stated values**; drawing labels transcribed with their attachment noted | rendered p.17; the 40 mm hole spacing rests on §8 prose, not on a labelled drawing dimension |
| Part-number references | **complete** | #64000, #64006-ES(b), #32420S, W25Q128JVSIM, P2X8C4M64PES |
| Code examples | **n/a — the guide contains none** | no listings to validate with `pnut_ts` |
| `pdf2md` (docling) leg | **complete — 17 of 17 pages** | whole-document runs were OOM-killed (exit 137) with ~10 GB of 12.9 GB committed by other work; **`pdfseparate` + one page at a time succeeded for all 17**. Output: `pdf2md-stripped.md`. Agrees with the OCR text and both camelot tables throughout, and reproduces the same OCR artefacts (`P59 A`/`P59 V`, "wnen") — which confirms those as OCR-side, not source-side |

**Unrecoverable content: none.** All 17 pages were read against their rendered page image.

### Trust Level Justification
✅ **GREEN** — Official Parallax documentation for production-approved hardware, and now
extracted with a tool chain that can carry its numerals. Trust the **re-extracted** artifacts
(`complete-p2-eval-board-reference.md`, `p2-eval-board-text.txt`); do **not** consume anything
under `archive/`. Carry the source's own internal contradictions (Pass 3) rather than resolving
them silently.

**EXTRACTION STATUS**: ✅ COMPLETE — as of the **2026-08-24 forced-OCR re-extraction**, measured
above. (The same line stood over the 2025 digit-free capture; it was false then.)
**TRUST LEVEL**: GREEN - Official Parallax hardware documentation
**INTEGRATION READY**: ✅ YES — from `complete-p2-eval-board-reference.md` + `p2-eval-board-text.txt`.
Anything derived from the pre-2026-08-24 extraction is **suspect until re-checked** (§0.6.2).
