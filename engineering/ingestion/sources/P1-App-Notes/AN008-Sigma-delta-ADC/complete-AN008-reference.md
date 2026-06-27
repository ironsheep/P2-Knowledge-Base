# AN008 — Sigma-delta Analog to Digital Conversion (Complete Reference)

> **Curated pass-1 summary.** Source: Parallax Semiconductor **Application Note AN008 v1.0** (© 2011 Parallax, Inc. dba Parallax Semiconductor). 10 pages. Platform: **Propeller 1 / P8X32A** (Spin1 + PASM1). Raw layout-preserving extract: `AN008-Sigma-delta-ADC-text.txt`. This file preserves the document's heading structure, derivation flow, equations, and authorial voice for the downstream P2 app-note style guide.

## Document identity
- **Title:** Sigma-delta Analog to Digital Conversion
- **Number / version:** AN008, v1.0 (Original document — Revision History lists only "Version 1.0").
- **Publisher:** Parallax Semiconductor (Parallax, Inc.), Rocklin CA. Contact block + trademark/copyright boilerplate on the masthead and final page.
- **Abstract (verbatim):** "Perform basic sigma-delta analog to digital conversion with any of the P8X32A's eight cogs, on any pair of I/O pins, and with a few inexpensive passive components. Variations on this simple technique include calibration options, multiple analog inputs, converting from AC sources such as a microphone, and accommodating extended input voltage ranges."

## Heading / section structure (as printed)
1. **Introduction** — each cog has two configurable counter modules; + external passives → sigma-delta ADC.
2. **Sigma-Delta Principle** — derives the technique from the inverting op-amp, then the CMOS D flip-flop analog.
3. **Propeller Sigma-Delta Application**
   - *Counter Registers* — CNT, CTRx/FRQx/PHSx; the "positive with feedback" mode.
   - *Hardware Configuration* — the standard gain-reduced RC circuit (Fig 4); duty-cycle margins.
   - *Layout Considerations* — SMT placement near the pins (Fig 5 photo).
   - *Software Procedure* — setup steps + the 5-step PASM acquisition sequence; **Listing 1**.
4. **Calibration** — hardware options (Fig 6 resistor, Fig 7 analog MUX); two software approaches (Spin scaling vs binary-search of `interval`); **Listing 2**.
5. **Variations on a Theme**
   - *Multiple Inputs* (Fig 8) · *Converting from AC Sources* (Fig 9, the Demo Board mic circuit) · *Extended Voltage Ranges* (Fig 10 + Eqs 1-2).
6. **Resources** · **References** · **Revision History** · legal boilerplate.

## The derivation (the heart of the note — voice-bearing)
The note teaches the principle by **analogy stacking**, not by formula-first:

1. **Op-amp anchor (Fig 1).** Start from the inverting op-amp the reader already knows: the output moves to hold the summing junction (− input) equal to the + input (Vdd/2), regardless of the analog input. Zero input → output = Vdd; Vdd input → output = 0.
2. **Replace the op-amp with a clocked CMOS D flip-flop (Fig 2).** Negative feedback from /Q (filtered by a cap) holds the summing junction near the D-input threshold Vdd/2. The /Q pin emits a pulse train whose **average duty cycle is proportional to the correction needed**. Worked example: analog = Vdd/4 → /Q must be 75% high. Because /Q is inverted, it's the **Q** duty cycle that tracks the input.
3. **Measurement is just counting.** "This duty cycle can be measured simply by counting the number of times the Q output is high for a given number of clocks. This, then, is the essence of sigma-delta analog-to-digital conversion." → maps directly onto a Propeller counter in positive-with-feedback mode.

## Propeller hardware mapping (P1-specific facts)
- **CNT** — global 32-bit count register, +1 per system clock tick, rolls over at `$FFFF_FFFF` (2³² − 1); one full cycle ≈ **53 s @ 80 MHz**.
- **Per cog: two counters**, each = three special-function registers **CTRx, FRQx, PHSx** (x = A or B).
- **CTRx mode for sigma-delta = "positive with feedback"** (`%01001` in the mode field): counter counts up on every clock where its input pin is high, AND the **output pin is driven to the inverse of the input pin, delayed by one clock** (the feedback action that replaces the flip-flop).
- **CTRx register layout (Fig 3):** mode field `%01001` (bits 30..26), a Destination field carrying the **Feedback Pin** number (bits ~13..9... the feedback/output pin), and a Source field carrying the **Input Pin** number (bits 8..0). Set via `MOVI ctra,#%0_01001_000` / `MOVD ctra,#FB_PIN` / `MOVS ctra,#INP_PIN`.
- **FRQx = 1** typically; **PHSx** accumulates +FRQx each clock the input is high → PHSx becomes the running high-count.
- **Conversion sequence (PASM, 5 steps):** copy CNT→`time`, +16; `WAITCNT time,interval` (sync); `NEG acc,phsa`; `WAITCNT time,#0` (wait the window); `ADD acc,phsa`. Net = how much PHSx grew over `interval` clocks ∝ input voltage (+ offset).
- **Precision ↔ interval:** interval 256 → ~8 bits, 512 → ~9 bits, etc. Because input gain < unity, interval must be scaled up to map 0..Vdd onto the bit range.

## Hardware / circuit facts
- **Standard circuit (Fig 4):** 150K input resistor, 100K feedback resistor, **two 1 nF caps** at the summing junction — one to ground **and one to Vdd** (the Vdd cap rejects rail noise that would otherwise unbalance the junction asymmetrically). Gain < unity so the full 0..Vdd range fits without clipping.
- **Duty-cycle margins:** analog = 0 → feedback duty ≈ **83.33%**; analog = Vdd → ≈ **16.67%**. The margin at both extremes absorbs threshold/level variation.
- **Layout (Fig 5):** keep passives very close to the input/feedback pins; SMT preferred. The Q44 package corner physically separates the chosen input and output pins to reduce capacitive coupling.

## Calibration
- **Why:** real thresholds aren't exactly Vdd/2 and rails aren't exactly 0/Vdd → calibrate to the input-range endpoints.
- **Hardware options:** (a) an extra Propeller pin via resistor **R** to inject Vss/Vdd endpoints (Fig 6) — R large enough not to overload, small enough not to skew gain when tri-stated; (b) a **4:1 analog MUX** (Fig 7) to select calibration inputs without loading concerns.
- **Software option 1 — Spin scaling (simplest):** pick an interval known to exceed the needed precision, then scale: `scaled := (raw - vlo) * RANGE / (vhi - vlo) #> 0 <# RANGE`. RANGE need not be a power of two. Disadvantages: LSB non-linearities unless interval ≫ RANGE; longer conversion time.
- **Software option 2 — binary search of interval (Listing 2):** successively sample Vdd and Vss with candidate intervals, halving a delta each pass (`SUMNC`), until the measured span equals the desired RANGE with only an offset correction (no scaling). A **`soak`** delay after each calibration-pin step lets the junction/feedback re-equalize. Optional clamp: `MAXS acc,range` / `MINS acc,#0`.

## Variations
- **Multiple inputs (Fig 8):** one feedback pin can serve several input RC front-ends; switch by reloading the **source field (bits 8..0) of CTRx** with the new input pin. Caveat: delay after switching so the new input's summing-junction caps recharge to threshold. With calibration, a MUX may be more pin-efficient.
- **AC sources (Fig 9):** inputs need not be DC-coupled; capacitive coupling works — this is exactly the **Propeller Demo Board (#32100) microphone input** circuit (electret mic, 10K, 0.1uF, 1nF, 100K).
- **Extended voltage ranges (Fig 10):** larger input resistor and/or a pull-up/pull-down bias resistor shift/widen the range. Standard 150K input → nominal range **−0.825 V to +4.125 V**, centered on the **1.65 V (Vdd/2 @ 3.3 V)** threshold. To recenter (e.g. 0..+10 V around +5 V), add bias resistors R1/R2 solved from the balance equations:
  - `R1 = 100·(VHI − VLO) / 3.3  kΩ`
  - `R2 = 100·(VHI − VLO) / (VHI + VLO − 3.3)  kΩ`
  - Worked: extend limits ±50% (range −2.5..+12.5 V) → **R1 ≈ 455 kΩ, R2 ≈ 224 kΩ**. If R2 comes out negative, flip its sign and make it a pull-**up** to Vdd; if infinite, omit it.
  - *(Equation operator-grouping transcribed from a fraction-mangling text layer — verify against `page-09.png` before downstream reuse; flagged as a gap.)*

## Code
Two in-PDF listings (Spin1 + PASM1), captured-not-compiled (no P1 compiler) — see `assets/code-2026-06-27/`. The *Resources* section also points to a downloadable code-archive ZIP at `www.parallaxsemiconductor.com/an008` (not provided to this ingestion).

## References (as printed)
1. AN001: Propeller P8X32A Counters — `www.parallaxsemiconductor.com/an001`
2. Propeller Demo Board; Parallax #32100 — `www.parallax.com`

## Voice / structure profile (for the P2 app-note style guide)
- **Register:** confident, peer-to-engineer, lightly conversational ("Now, replace the op amp…", "This, then, is the essence of…", "say, interval would ideally equal 256"). Assumes an EE-literate reader; bridges *from* a known analog circuit *to* the digital technique.
- **Pedagogy = analogy ladder:** op-amp → flip-flop → counter. Each figure advances one rung. Worked numeric examples (Vdd/4 → 75%; 83.33%/16.67% margins; R1≈455k/R2≈224k) ground every abstract claim.
- **Structure:** principle → hardware mapping → minimal listing → refinement (calibration) → richer listing → "Variations on a Theme" breadth section. Consistent **Figure N: Title** captions; numbered procedure steps; equations called out as "Equation 1a/1b/2a/2b."
- **Tone toward the chip:** treats the Propeller's counter hardware as the enabling trick; emphasizes "a few inexpensive passive components" and SMT layout pragmatics. Practical, build-it framing throughout.
