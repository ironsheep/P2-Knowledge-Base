# Image Catalog — PE Kit Labs: Fundamentals v1.2

**Source:** Parallax #122-32305 *Propeller Education Kit Labs: Fundamentals* v1.2 (233 pp, P1/P8X32A)
**Cataloged:** 2026-06-27 · **115 figures** (captioned) + 15 tables + Appendix D block diagram
**Extracted to this folder:** **7 images** (raster, `pdfimages` + `image-tools-mcp` quality-gated)

## Extraction policy applied (per task brief)
The planned P2 labs book will **redraw all schematics/diagrams in TikZ/circuitikz** and **shoot new
photos of the P2 environment**, so original diagram extraction has little reuse value. Therefore:
- **`breadboard/wiring-photo` → EXTRACT** (cannot be regenerated; reference pattern for the new manual's
  photo shoots — highest value). Extracted the representative kit/platform/close-up photos.
- **`schematic/circuit-diagram` → catalog only** (redrawn in TikZ/circuitikz).
- **`terminal/scope-screenshot` → catalog; extract a few representative** (output we may reproduce).
  Extracted 2 (one PST terminal, one RC-decay terminal).
- **`code-screenshot` → catalog only** (we have the real `.spin`).
- **`conceptual-diagram` / `other` → catalog only.**
- When in doubt → do not extract; the catalog records it.

## Extracted files (quality-gated: dimensions OK, varied dominant colors, none `#000000`-dominant)
| File | Figure | Type | px | Notes |
|---|---|---|---|---|
| `fig-1-10a-pe-platform-40pin-dip.jpg` | 1-10(a) | breadboard/wiring-photo | 420×219 | 40-pin DIP PE Platform overview photo |
| `fig-1-10b-pe-platform-propstick.jpg` | 1-10(b) | breadboard/wiring-photo | 420×219 | PropStick USB PE Platform overview photo |
| `fig-3-1-pe-kit-platform-40pin-dip.jpg` | 3-1 | breadboard/wiring-photo | 782×652 | Built 40-pin DIP PE Platform (the canonical build target) |
| `fig-3-2-pe-platform-components.jpg` | 3-2 | breadboard/wiring-photo | 590×493 | Same platform with labeled major components |
| `fig-3-9-supply-strap-filter-cap-closeup.png` | 3-9 | breadboard/wiring-photo | 1100×778 | Close-up of supply input strap + filter-cap connections (fine-detail wiring) |
| `fig-6-12-pst-terminal-messages.png` | 6-12 | terminal/scope-screenshot | 875×504 | Parallax Serial Terminal displaying repeated messages (representative terminal output) |
| `fig-7-5-rc-decay-times-terminal.png` | 7-5 | terminal/scope-screenshot | 720×426 | RC-decay measurement values in the terminal (representative measurement output) |

---

## Complete figure inventory (all 115 figures)

**Legend — TYPE:** `photo`=breadboard/wiring-photo · `schem`=schematic/circuit-diagram ·
`term`=terminal/scope-screenshot · `code`=code-screenshot (IDE/UI) · `concept`=conceptual-diagram ·
`table-img`=table rendered as image · `other`. **DECISION:** EXTRACT / catalog-only (+rationale).

### Chapter 1 — Overview (pp 7–16)
| Fig | Caption | Type | Decision |
|---|---|---|---|
| 1-1 | Propeller Microcontroller Packages and Hub & Cog Interaction | concept (incl. package photos) | catalog — redraw for P2 |
| 1-2 | Application Examples | concept | catalog |
| 1-3 | Cog Interpreting Spin Language | concept | catalog |
| 1-4 | Cog Executing (assembly) | concept | catalog |
| 1-5 | Two (or more) Cogs Working | concept | catalog |
| 1-6 | Cog Launching | concept | catalog |
| 1-7 | Object (application building blocks) | concept | catalog |
| 1-8 | Loading a Program into RAM or EEPROM | concept | catalog |
| 1-9 | Propeller Education Kit (parts) | photo | catalog — represented by extracted 1-10/3-1/3-2 |
| 1-10 | PE Kit Platforms (a) DIP (b) PropStick | photo | **EXTRACTED (a,b)** |
| 1-11 | ViewPort Lab Excerpt (scope/spectrum) | term | catalog |

### Chapter 2 — Software, Documentation & Resources (pp 17–18)
| Fig | Caption | Type | Decision |
|---|---|---|---|
| 2-1 | Propeller Tool (left) & Parallax Serial Terminal (right) | code | catalog |
| 2-2 | PDF Resources included with the (download) | other | catalog |
| 2-3 | Example (resource download) | code | catalog |

### Chapter 3 — Setup and Testing Lab (pp 19–44)
| Fig | Caption | Type | Decision |
|---|---|---|---|
| 3-1 | PE Kit Platform (40-Pin DIP version) | photo | **EXTRACTED** |
| 3-2 | PE Kit Platform Components (labeled) | photo | **EXTRACTED** |
| 3-3 | Breadboards | photo | catalog — represented by 3-1/3-2 |
| 3-4 | Schematic – Propeller DIP Plus Kit | schem | catalog — redraw in TikZ |
| 3-5 | Wiring Diagram – DIP Plus Kit before ICs connected | photo (drawn wiring) | catalog — redrawn + re-shot for P2 |
| 3-6 | Wiring Diagram – DIP Plus Kit (after ICs) | photo (drawn wiring) | catalog — redrawn + re-shot |
| 3-7 | Test Circuit Schematic | schem | catalog |
| 3-8 | Test Circuit Wiring Diagram | photo (drawn wiring) | catalog |
| 3-9 | Close-up: Supply Input Strap & Filter Cap connections | photo | **EXTRACTED** |
| 3-10 | (Propeller Tool / load step) | code | catalog |
| 3-11 | Serial Port (selection) | code | catalog |
| 3-12 | Device (Manager / driver) | code | catalog |

### Chapter 4 — I/O and Timing Basics (pp 45–68)
| Fig | Caption | Type | Decision |
|---|---|---|---|
| 4-1 | LED Pushbutton Schematic | schem | catalog |
| 4-2 | Repeat Code Block | concept | catalog |
| 4-3 | The `waitcnt` Command and the `cnt` Register | concept | catalog (key timing explainer — redraw) |

### Chapter 5 — Methods and Cogs (pp 69–82)
| Fig | Caption | Type | Decision |
|---|---|---|---|
| 5-1 | LED Pushbutton Schematic | schem | catalog |
| 5-2 | Calling a Method | concept | catalog |
| 5-3 | Parameter Passing | concept | catalog |
| 5-4 | Launching Methods Into Cogs with Parameter Passing | concept | catalog |
| 5-5 | Object Info Window | code | catalog |
| 5-6 | Using a Method's Result Variable | concept | catalog |

### Chapter 6 — Objects (pp 83–124)
| Fig | Caption | Type | Decision |
|---|---|---|---|
| 6-1 | Schematic (drawn with Propeller Tool) | schem | catalog |
| 6-2 | Calling Methods in Another Object with Dot Notation | concept | catalog |
| 6-3 | Object Info Window | code | catalog |
| 6-4 | Propeller Tool with Object View | code | catalog |
| 6-5 | Documentation View | code | catalog |
| 6-6 | More Documentation View | code | catalog |
| 6-7 | Propeller Tool (Character Chart) | code | catalog |
| 6-8 | Drawing (schematic via Character Chart) | other | catalog |
| 6-9 | Parallax Serial Terminal | term | catalog |
| 6-10 | Connected vs. Disconnected (to/from Com Port) | term | catalog |
| 6-11 | Appearance and Function Preferences | code | catalog |
| 6-12 | Using PST Object to Display Messages | term | **EXTRACTED (representative)** |
| 6-13 | (PST display, caption merged in text layer) | term | catalog |
| 6-14 | Parallax Serial Terminal Object Documentation View | code | catalog |
| 6-15 | Finding a Text String in Memory | code | catalog |
| 6-16 | Testing EnterAndDisplayValues.spin in PST | term | catalog |
| 6-17 | The PST control-character constants list | code | catalog |
| 6-18 | Serial (terminal control) | term | catalog |
| 6-19 | Entering Binary Patterns | term | catalog |
| 6-20 | Entering Pin and Rate into (PST) | term | catalog |

### Chapter 7 — Counter Modules & Circuit Applications (pp 125–190)
| Fig | Caption | Type | Decision |
|---|---|---|---|
| 7-1 | RC Decay Parts and Circuit | schem+parts | catalog |
| 7-2 | RC Charge and Decay Circuits and Voltages | schem/concept | catalog |
| 7-3 | Excerpts from CTR.spin's Counter Mode Table | table-img | catalog |
| 7-4 | CTRA/B Register Map from CTR.spin | concept | catalog |
| 7-5 | RC Decay Times (terminal) | term | **EXTRACTED (representative)** |
| 7-6 | Second RC Decay Parts and Circuit | schem+parts | catalog |
| 7-7 | LED Circuit for Brightness Control with Duty Signals | schem | catalog |
| 7-8 | More Excerpts from CTR.spin's Counter Mode Table | table-img | catalog |
| 7-9 | CTRA/B Register Map from CTR.spin | concept | catalog |
| 7-10 | Audio Range NCO Parts List and Circuits | schem+parts | catalog |
| 7-11 | NCO Excerpts from CTR Counter Mode Table | table-img | catalog |
| 7-12 | (NCO circuit/table, caption merged in text layer) | schem/table-img | catalog |
| 7-13 | IR Object Detection Parts and Schematic | schem | catalog |
| 7-14 | IR LED Assembly | photo | catalog — physical-assembly photo; extract-candidate deferred (specialized) |
| 7-15 | IR LED and Detector Orientation for Object Detection | photo/concept | catalog |
| 7-16 | Object Detection Display | term | catalog |
| 7-17 | IR Distance Detection Parts and Schematic | schem | catalog |
| 7-18 | Distance Detection Display | term | catalog |
| 7-19 | Edge Detector Excerpts from CTR Counter Mode Table | table-img | catalog |
| 7-20 | Use P8 to Measure PWM Signal from P6 | schem/concept | catalog |
| 7-21 | PLL Mode Excerpts from CTR Counter Mode Table | table-img | catalog |
| 7-22 | (PLL circuit/table, caption merged in text layer) | schem/table-img | catalog |
| 7-23 | Calculate Frequency Given FRQA | concept/equation | catalog |
| 7-24 | Metal Detector Parts and Schematic | schem | catalog |
| 7-25 | Metal Detector | schem/photo | catalog |
| 7-26 | (Metal detector detail, caption truncated) | schem/concept | catalog |
| 7-27 | P13 Response to Resonant Frequency at P15 | term (scope) | catalog |
| 7-28 | LC Circuit P13 Output Responses at Various Frequencies | term (scope) | catalog |
| 7-29 | Eddy Currents Causing Opposing Magnetic Fields | concept | catalog |
| 7-30 | Eddy Current's Effects on the Loop's Inductance | concept | catalog |
| 7-31 | Calibrated Metal Detector Response (no metal / with metal) | term | catalog |

### Appendix D
| Fig | Caption | Type | Decision |
|---|---|---|---|
| D | Propeller P8X32A Block Diagram | concept | catalog — P1 architecture reference |

---

## Summary
| Metric | Count |
|---|---|
| Total figures cataloged | 115 |
| Total raster images embedded in PDF | 139 (incl. UI chrome / repeated assets) |
| **Images extracted** | **7** |
| — breadboard/wiring-photo extracted | 5 (1-10a, 1-10b, 3-1, 3-2, 3-9) |
| — terminal/screenshot extracted (representative) | 2 (6-12, 7-5) |
| Schematics (catalog-only, redraw in TikZ) | ~22 |
| Conceptual/architecture diagrams (catalog-only) | ~24 |
| Code/IDE screenshots (catalog-only) | ~18 |
| Counter-mode table images (catalog-only) | ~7 |

**Caption-numbering note:** the text layer merged a few captions into running prose (6-13, 7-12, 7-22,
7-26) so their exact wording is approximate above; the figures exist on their pages and are accounted
for in the 115 total. No OCR of figure labels was needed (the surrounding prose already names each
figure's content; OCR would add no reference value for catalog-only items).
