# Smart Pins Tutorial - Punch List

**Document:** P2-Smart-Pins-Green-Book-Tutorial
**Purpose:** Track fixes and enhancements needed before final release

---

## Completed This Session (Dec 4, 2025)

- [x] **INDEX heading missing** - Was not appearing in PDF; now shows correctly
- [x] **Continuous page numbering** - Pages now number continuously (no reset at Part I)
- [x] **Output Generation Modes table** - Column overlap fixed
- [x] **Output Mode Flowchart** - Crossing arrows fixed (but see new issue below)
- [x] **Anti-pattern code blocks** - Chapter 5 examples now properly split into antipattern/spin2 blocks
- [x] **TikZ diagrams rendering** - All 13 unwrapped diagram macros now have `{=latex}` wrappers
- [x] **Appendix C math formulas** - Now render correctly with raw LaTeX wrapping
- [x] **Common Configurations table** - OR operator fixed (was showing `\{}`)
- [x] **Appendix A Quick Reference table** - Reduced to 4 columns, layout fixed

---

## Completed Previous Session

- [x] **Narrative text disappearing after PASM2 blocks** - Fixed `\uppercase` in lstset (p2kb-sp-code-coloring.lua)
- [x] **Part I centering/page break issue** - Fixed filter treating Part I as document title (p2kb-sp-fix-title-as-part.lua)
- [x] **Diagram 1 (DRVH timing)** - Fixed text overlap, Reg* spacing, label alignment
- [x] **Diagram 2 (TESTB INA timing)** - Fixed P0 IN overlap, Reg spacing, ALU/C/Z cramping
- [x] **Diagram 3 (TESTP timing)** - Fixed P0 IN overlap, Reg spacing, C/Z cramping
- [x] **Missing page headers** - Default `fancy` pagestyle had no header content defined; added chapter title and page number
- [x] **WRPIN D format ASCII art** - Replaced broken ASCII art (box-drawing chars not rendering) with TikZ bit-field diagram (`\WRPINFormatDiagram`)

---

## Pending - Layout/Formatting (HIGH PRIORITY)

- [ ] **Chapter 0 title still justified** - Words spread across page width
  - `\raggedright` fix in `\titleformat{\chapter}` not working
  - Need to investigate why title is still being justified
  - File: `templates/p2kb-sp-foundation.sty`

- [ ] **First chapter after part breaking to new page** - Should stay on same page as Part title
  - Algorithm in `\pretocmd{\chapter}` for `\iffirstchapterinpart` not working
  - Chapter 0 should appear on same page as "Part I: Fundamentals"
  - File: `templates/p2kb-sp-foundation.sty`

- [ ] **Vertical whitespace before chapter headings** - Unwanted space above chapters on new pages
  - `\titlespacing*{\chapter}` has `{0pt}` for space before, but space still appears
  - Need to eliminate vertical space at top of page for chapters

- [ ] **List spacing before first item** - Still too much gap before first bullet
  - `enumitem` package with `\setlist{topsep=0pt}` not taking effect
  - Need to investigate why list spacing fix isn't working
  - File: `templates/p2kb-sp-foundation.sty`

- [ ] **Figure captions** - Add centered, bold "Figure N: Title" below each diagram
  - Approach: Use LaTeX `figure` environment with `\caption{}`
  - Requires: `\captionsetup{labelfont=bf, font=small, justification=centering}`
  - Decision needed: Automatic numbering vs manual titles

---

## Pending - Diagram Fixes

### URGENT: Flowchart Regression
- [ ] **Output Mode Flowchart** - Line passing across "Phase Correct" diamond
  - Previous fix resolved crossing arrows but introduced new problem
  - Line goes horizontally across face of diamond instead of proper Yes/No routing
  - File: `templates/p2kb-sp-diagrams.sty` - `\OutputModeFlowchart`

### TikZ Diagram Review Checklist
**Verify each diagram accurately represents its source PNG**

#### Timing & Signal Diagrams (Chapter 0)
- [ ] `\DRVHTimingDiagram` (line 229) - Basic I/O output timing
- [ ] `\TESTBINATimingDiagram` (line 237) - Basic I/O input sampling
- [ ] `\TESTPTimingDiagram` (line 243) - TESTP timing

#### Configuration Diagrams (Chapter 2)
- [ ] `\WRPINFormatDiagram` (lines 683, 812, 5069) - WRPIN D format bit fields

#### Mode-Specific Diagrams (Chapters 3-4)
- [ ] `\DACPWMPeriodDiagram` (line 1246) - DAC PWM period
- [ ] `\PulseWidthMeasurementDiagram` (line 1351) - Pulse width measurement
- [ ] `\NCOFrequencyDiagram` (line 1478) - NCO frequency
- [ ] `\NCODutyTimingDiagram` (line 1563) - NCO duty timing
- [ ] `\NCODutyBlockDiagram` (line 1569) - NCO duty block
- [ ] `\TrianglePWMDiagram` (line 1631) - Triangle PWM
- [ ] `\SawtoothPWMDiagram` (line 1689) - Sawtooth PWM
- [ ] `\QuadEncoderDiagram` (line 1987) - Quadrature encoder
- [ ] `\PeriodMeasurementDiagram` (line 2068) - Period measurement
- [ ] `\SinglePhaseEncoderDiagram` (line 2168) - Single phase encoder
- [ ] `\ComparatorDiagram` (line 2201) - Comparator
- [ ] `\ContinuousPeriodDiagram` (line 2253) - Continuous period
- [ ] `\TimeoutWatchdogDiagram` (line 2325) - Timeout watchdog
- [ ] `\DualInputTimeDiagram` (line 2331) - Dual input time
- [ ] `\ADCSampleHoldDiagram` (line 2439) - ADC sample/hold
- [ ] `\USBDifferentialDiagram` (line 2500) - USB differential
- [ ] `\SyncSerialFallingDiagram` (line 2530) - Sync serial falling edge
- [ ] `\SyncSerialRisingDiagram` (line 2536) - Sync serial rising edge

#### Advanced Technique Diagrams (Chapter 5)
- [ ] `\FeedbackLoopDiagram` (line 3027) - Feedback loop
- [ ] `\ClockDistributionDiagram` (line 3060) - Clock distribution
- [ ] `\ProtocolBridgeDiagram` (line 3086) - Protocol bridge
- [ ] `\StateMachineDiagram` (line 3113) - State machine

#### Application Diagrams (Part III)
- [ ] `\MotorControllerDiagram` (line 4168) - Motor controller
- [ ] `\DataAcquisitionDiagram` (line 4251) - Data acquisition
- [ ] `\CommunicationHubDiagram` (line 4311) - Communication hub
- [ ] `\SynchronizedSamplingDiagram` (line 4384) - Synchronized sampling
- [ ] `\OscilloscopeArchDiagram` (line 4633) - Oscilloscope architecture
- [ ] `\RobotSystemDiagram` (line 4752) - Robot system
- [ ] `\CompleteSystemDiagram` (line 4877) - Complete system

**Total: 31 unique diagrams to review**

---

## Pending - Content

- [ ] **Code line overflow** - Audit all PASM2 and Spin2 code blocks for lines exceeding ~76 characters
  - Lines longer than 76 chars overflow the code box boundaries in PDF
  - Need document-wide pass to identify and wrap/shorten offending lines
  - Similar fix applied successfully to other documents

- [ ] **PASM2 instruction mnemonic uppercasing** - Adopt the Lua filter from De Silva Manual
  - De Silva Manual has a Lua filter that uppercases instruction mnemonics in PASM2 code blocks
  - Port that filter to Smart Pins for consistent presentation
  - Reference: `p2-pasm-desilva-style` workspace Lua filters

- [ ] **Missing mode narratives** - Ensure all 32 Smart Pin modes have full tutorial content
  - Mode %10000 (P_TIME_STATES) - Currently stub, needs full narrative
  - Mode %10001 (P_TIME_HIGHS) - Currently stub, needs full narrative
  - Mode %10100 (P_PERIODS_HIGHS) - Currently stub, needs full narrative
  - Mode %10101 (P_COUNTER_TICKS) - Currently stub, needs full narrative
  - Mode %10110 (P_COUNTER_HIGHS) - Currently stub, needs full narrative
  - Mode %10111 (P_COUNTER_PERIODS) - Currently stub, needs full narrative
  - Audit all modes for completeness (Quick Reference, explanation, use cases, code examples)
  - Use P2 Knowledge Base YAMLs as source for accurate technical details

---

## Pending - Tooling

- [ ] **LaTeX escape script: Add `$$...$$` math protection**
  - Location: `/engineering/tools/conversion/latex_escape_processor.py`
  - Problem: Script escapes `$` to `\$` which breaks LaTeX display math
  - Current workaround: Wrap math in ```` ```{=latex} ```` raw blocks
  - Script already protects `\(...\)` and `\[...\]` (lines 211-212) but not `$$`
  - **Test case to add to regression suite:**
    ```markdown
    **NCO Frequency:**

    $$\text{Frequency} = \frac{X \times \text{ClockFreq}}{2^{32}}$$
    ```
  - Expected: `$$` delimiters and content pass through unchanged
  - Current failure: `$` becomes `\$`, breaking the math
  - Fix approach: Add pattern to protect `$$...$$` blocks similar to how `\[...\]` is protected
  - Related: May also want to protect inline math `$...$` (single dollar signs)

---

## Notes

Files modified this session:
- `P2-Smart-Pins-Green-Book-Tutorial.md` - Tables, diagrams, anti-patterns, math, INDEX
- `templates/p2kb-sp-foundation.sty` - Pagination, list spacing, raggedright (some fixes not working)
- `templates/p2kb-sp-diagrams.sty` - Flowchart fix (introduced new issue)
- `filters/p2kb-sp-frontmatter.lua` - Continuous page numbering
- `PUNCH-LIST.md` - This file

---

*Created: 2025-12-03*
*Last Updated: 2025-12-04*
